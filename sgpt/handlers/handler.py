import json
from pathlib import Path
from typing import Any, Callable, Dict, Generator, List, Optional

from ..cache import Cache
from ..config import cfg
from ..function import get_function
from ..printer import MarkdownPrinter, Printer, TextPrinter
from ..role import DefaultRoles, SystemRole
from ..backends.factory import build_completion_callable
from ..backends.router import should_use_deepseek
from ..backends.streaming import get_delta_tool_calls
from ..backends.tools import make_assistant_tool_request_message, make_tool_result_message

completion: Callable[..., Any]


def _uninitialized_completion(*args: Any, **kwargs: Any) -> Any:
    raise RuntimeError(
        "LLM client not initialized. This is a bug: completion() was called "
        "before backend initialization."
    )


# NOTE: Tests monkeypatch `sgpt.handlers.handler.completion`, so this name must
# exist at import time, but it must not require any API keys at import time.
completion = _uninitialized_completion


class Handler:
    cache = Cache(
        int(cfg.get_optional("CACHE_LENGTH", "100") or "100"),
        Path(cfg.get_optional("CACHE_PATH", str(Path.home() / ".cache" / "sgpt"))
        or str(Path.home() / ".cache" / "sgpt")),
    )

    def __init__(self, role: SystemRole, markdown: bool) -> None:
        self.role = role

        api_base_url = cfg.get_required("API_BASE_URL")
        self.base_url = None if api_base_url == "default" else api_base_url
        self.timeout = int(cfg.get_required("REQUEST_TIMEOUT"))
        self.default_api = cfg.get_required("DEFAULT_API")
        self.use_litellm = cfg.get_required("USE_LITELLM") == "true"

        self.markdown = "APPLY MARKDOWN" in self.role.role and markdown
        self.code_theme, self.color = (
            cfg.get_required("CODE_THEME"),
            cfg.get_required("DEFAULT_COLOR"),
        )

    @property
    def printer(self) -> Printer:
        return (
            MarkdownPrinter(self.code_theme)
            if self.markdown
            else TextPrinter(self.color)
        )

    def make_messages(self, prompt: str) -> List[Dict[str, str]]:
        raise NotImplementedError

    def handle_function_call(
        self,
        messages: List[dict[str, Any]],
        name: str,
        arguments: str,
    ) -> Generator[str, None, None]:
        import uuid

        tool_call_id = str(uuid.uuid4())

        messages.append(
            make_assistant_tool_request_message(
                default_api=self.default_api,
                tool_call_id=tool_call_id,
                name=name,
                arguments=arguments,
            )
        )

        if messages and messages[-1]["role"] == "assistant":
            yield "\n"

        dict_args = json.loads(arguments)
        joined_args = ", ".join(f'{k}="{v}"' for k, v in dict_args.items())
        yield f"> @FunctionCall `{name}({joined_args})` \n\n"

        result = get_function(name)(**dict_args)
        if cfg.get("SHOW_FUNCTIONS_OUTPUT") == "true":
            yield f"```text\n{result}\n```\n"

        messages.append(
            make_tool_result_message(
                default_api=self.default_api,
                tool_call_id=tool_call_id,
                name=name,
                result=result,
            )
        )

    @cache
    def get_completion(
        self,
        model: str,
        temperature: float,
        top_p: float,
        messages: List[Dict[str, Any]],
        functions: Optional[List[Dict[str, str]]],
        caching: bool = True,
    ) -> Generator[str, None, None]:
        global completion

        name = arguments = ""
        is_shell_role = self.role.name == DefaultRoles.SHELL.value
        is_code_role = self.role.name == DefaultRoles.CODE.value
        is_dsc_shell_role = self.role.name == DefaultRoles.DESCRIBE_SHELL.value
        if is_shell_role or is_code_role or is_dsc_shell_role:
            functions = None

        default_model = cfg.get_required("DEFAULT_MODEL")
        if should_use_deepseek(
            model=model,
            default_api=self.default_api,
            default_model=default_model,
        ):

            # Initialize backend only if not already monkeypatched (tests patch
            # `completion` directly).
            if completion is _uninitialized_completion:
                deepseek_api_key = cfg.get_optional("DEEPSEEK_API_KEY")
                deepseek_api_base = cfg.get_required("DEEPSEEK_API_BASE_URL")
                if not deepseek_api_key:
                    raise ValueError(
                        "DEEPSEEK_API_KEY is required when using DeepSeek API"
                    )

                completion = build_completion_callable(
                    provider="deepseek",
                    api_key=deepseek_api_key,
                    base_url=deepseek_api_base,
                    timeout=self.timeout,
                )

            deepseek_kwargs: dict[str, Any] = {}
            if functions:
                deepseek_kwargs = {
                    "tool_choice": "auto",
                    "tools": functions,
                    "parallel_tool_calls": False,
                }

            response = completion(
                model=model,
                temperature=temperature,
                top_p=top_p,
                messages=messages,
                stream=True,
                **deepseek_kwargs,
            )
        else:
            # Default API (OpenAI or LiteLLM)

            if completion is _uninitialized_completion:
                openai_api_key = cfg.get_optional("OPENAI_API_KEY")
                if not self.use_litellm and not openai_api_key:
                    raise ValueError(
                        "OPENAI_API_KEY is required when using OpenAI backend"
                    )

                completion = build_completion_callable(
                    provider="openai",
                    api_key=openai_api_key or "",
                    base_url=self.base_url,
                    timeout=self.timeout,
                    use_litellm=self.use_litellm,
                )

            call_kwargs: dict[str, Any] = {}
            if functions:
                call_kwargs = {
                    "tool_choice": "auto",
                    "tools": functions,
                    "parallel_tool_calls": False,
                }

            response = completion(
                model=model,
                temperature=temperature,
                top_p=top_p,
                messages=messages,
                stream=True,
                **call_kwargs,
            )

        try:
            for chunk in response:
                delta = chunk.choices[0].delta

                # LiteLLM uses dict instead of Pydantic object like OpenAI does.
                tool_calls = get_delta_tool_calls(delta, use_litellm=self.use_litellm)
                if tool_calls:
                    for tool_call in tool_calls:
                        if tool_call.function.name:
                            name = tool_call.function.name
                        if tool_call.function.arguments:
                            arguments += tool_call.function.arguments
                if chunk.choices[0].finish_reason in ["tool_calls", "function_calls"]:
                    yield from self.handle_function_call(messages, name, arguments)
                    yield from self.get_completion(
                        model=model,
                        temperature=temperature,
                        top_p=top_p,
                        messages=messages,
                        functions=functions,
                        caching=False,
                    )
                    return

                yield delta.content or ""
        except KeyboardInterrupt:
            response.close()

    def handle(
        self,
        prompt: str,
        model: str,
        temperature: float,
        top_p: float,
        caching: bool,
        functions: Optional[List[Dict[str, str]]] = None,
        **kwargs: Any,
    ) -> str:
        disable_stream = cfg.get_required("DISABLE_STREAMING") == "true"
        messages = self.make_messages(prompt.strip())
        generator = self.get_completion(
            model=model,
            temperature=temperature,
            top_p=top_p,
            messages=messages,
            functions=functions,
            caching=caching,
            **kwargs,
        )
        return self.printer(generator, not disable_stream)

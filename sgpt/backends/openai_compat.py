from __future__ import annotations

from typing import Any, Callable


def openai_chat_completion_callable(
    *, api_key: str, timeout: int, base_url: str | None = None
) -> Callable[..., Any]:
    """Create an OpenAI-compatible chat completion callable.

    This is used for both OpenAI and OpenAI-compatible providers (e.g. DeepSeek).
    """

    from openai import OpenAI

    kwargs: dict[str, Any] = {"api_key": api_key, "timeout": timeout}
    if base_url is not None:
        kwargs["base_url"] = base_url

    client = OpenAI(**kwargs)
    return client.chat.completions.create

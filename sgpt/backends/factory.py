from __future__ import annotations

from typing import Any, Callable

from sgpt.backends.litellm_backend import litellm_completion_callable
from sgpt.backends.openai_compat import openai_chat_completion_callable


def build_completion_callable(
    *,
    provider: str,
    api_key: str,
    timeout: int,
    base_url: str | None = None,
    use_litellm: bool = False,
) -> Callable[..., Any]:
    """Return a streaming completion callable for the requested provider.

    `provider` is informational for now; the returned callable matches the OpenAI
    Python SDK / LiteLLM completion calling convention used throughout the app.
    """

    if use_litellm:
        return litellm_completion_callable()

    return openai_chat_completion_callable(api_key=api_key, timeout=timeout, base_url=base_url)

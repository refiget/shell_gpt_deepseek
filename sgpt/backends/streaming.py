from __future__ import annotations

from typing import Any


def get_delta_tool_calls(delta: Any, *, use_litellm: bool) -> Any:
    """Extract tool_calls from a streaming delta.

    OpenAI SDK returns pydantic objects (delta.tool_calls).
    LiteLLM returns plain dicts (delta.get("tool_calls")).
    """

    if use_litellm:
        return delta.get("tool_calls")
    return delta.tool_calls

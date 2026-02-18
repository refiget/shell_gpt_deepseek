from __future__ import annotations

from typing import Any


def is_deepseek_api(default_api: str) -> bool:
    return default_api == "deepseek"


def make_assistant_tool_request_message(
    *,
    default_api: str,
    tool_call_id: str,
    name: str,
    arguments: str,
) -> dict[str, Any]:
    """Return the assistant message that represents a tool/function call.

    DeepSeek (OpenAI-compatible) uses `tool_calls`.
    Older OpenAI function-calling used `function_call`.

    Keeping this logic centralized makes it easier to support additional
    providers.
    """

    if is_deepseek_api(default_api):
        return {
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {
                    "id": tool_call_id,
                    "type": "function",
                    "function": {"name": name, "arguments": arguments},
                }
            ],
        }

    return {
        "role": "assistant",
        "content": "",
        "function_call": {"name": name, "arguments": arguments},
    }


def make_tool_result_message(
    *, default_api: str, tool_call_id: str, name: str, result: str
) -> dict[str, Any]:
    """Return the message carrying a tool/function result back to the model."""

    if is_deepseek_api(default_api):
        return {
            "role": "tool",
            "content": result,
            "tool_call_id": tool_call_id,
            "name": name,
        }

    return {"role": "function", "content": result, "name": name}

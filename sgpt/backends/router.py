from __future__ import annotations


def should_use_deepseek(*, model: str, default_api: str, default_model: str) -> bool:
    """Return True if the request should be routed to the DeepSeek API.

    Routing rules (back-compat with current behavior):
    - If the model name is explicitly a DeepSeek model (prefix `deepseek-`) -> DeepSeek.
    - Otherwise, only route to DeepSeek when the user did not override the model,
      i.e. model == DEFAULT_MODEL, and DEFAULT_API is deepseek.

    This allows `--model gpt-4-*` to select the OpenAI backend even if
    DEFAULT_API=deepseek.
    """

    if model.startswith("deepseek-"):
        return True

    return default_api == "deepseek" and model == default_model

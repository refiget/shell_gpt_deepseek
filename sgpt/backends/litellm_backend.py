from __future__ import annotations

from typing import Any, Callable


def litellm_completion_callable() -> Callable[..., Any]:
    import litellm  # type: ignore

    litellm.suppress_debug_info = True
    return litellm.completion

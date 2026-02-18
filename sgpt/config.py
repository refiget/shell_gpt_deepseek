import os
from pathlib import Path
from tempfile import gettempdir
from typing import Any

from click import UsageError

CONFIG_FOLDER = os.path.expanduser("~/.config")
SHELL_GPT_CONFIG_FOLDER = Path(CONFIG_FOLDER) / "shell_gpt"
SHELL_GPT_CONFIG_PATH = SHELL_GPT_CONFIG_FOLDER / ".sgptrc"
ROLE_STORAGE_PATH = SHELL_GPT_CONFIG_FOLDER / "roles"
FUNCTIONS_PATH = SHELL_GPT_CONFIG_FOLDER / "functions"
CHAT_CACHE_PATH = Path(gettempdir()) / "chat_cache"
CACHE_PATH = Path(gettempdir()) / "cache"

# TODO: Refactor ENV variables with SGPT_ prefix.
DEFAULT_CONFIG: dict[str, Any] = {
    # TODO: Refactor it to CHAT_STORAGE_PATH.
    "CHAT_CACHE_PATH": os.getenv("CHAT_CACHE_PATH", str(CHAT_CACHE_PATH)),
    "CACHE_PATH": os.getenv("CACHE_PATH", str(CACHE_PATH)),
    "CHAT_CACHE_LENGTH": int(os.getenv("CHAT_CACHE_LENGTH", "100")),
    "CACHE_LENGTH": int(os.getenv("CHAT_CACHE_LENGTH", "100")),
    "REQUEST_TIMEOUT": int(os.getenv("REQUEST_TIMEOUT", "60")),
    "DEFAULT_MODEL": os.getenv("DEFAULT_MODEL", "deepseek-chat"),
    "DEFAULT_COLOR": os.getenv("DEFAULT_COLOR", "magenta"),
    "DEFAULT_API": os.getenv("DEFAULT_API", "deepseek"),
    "ROLE_STORAGE_PATH": os.getenv("ROLE_STORAGE_PATH", str(ROLE_STORAGE_PATH)),
    "DEFAULT_EXECUTE_SHELL_CMD": os.getenv("DEFAULT_EXECUTE_SHELL_CMD", "false"),
    "DISABLE_STREAMING": os.getenv("DISABLE_STREAMING", "false"),
    "CODE_THEME": os.getenv("CODE_THEME", "dracula"),
    "OPENAI_FUNCTIONS_PATH": os.getenv("OPENAI_FUNCTIONS_PATH", str(FUNCTIONS_PATH)),
    "OPENAI_USE_FUNCTIONS": os.getenv("OPENAI_USE_FUNCTIONS", "true"),
    "SHOW_FUNCTIONS_OUTPUT": os.getenv("SHOW_FUNCTIONS_OUTPUT", "false"),
    "API_BASE_URL": os.getenv("API_BASE_URL", "default"),
    "DEEPSEEK_API_KEY": os.getenv("DEEPSEEK_API_KEY"),
    "DEEPSEEK_API_BASE_URL": os.getenv(
        "DEEPSEEK_API_BASE_URL", "https://api.deepseek.com/v1"
    ),
    "PRETTIFY_MARKDOWN": os.getenv("PRETTIFY_MARKDOWN", "true"),
    "USE_LITELLM": os.getenv("USE_LITELLM", "false"),
    "SHELL_INTERACTION": os.getenv("SHELL_INTERACTION", "true"),
    "OS_NAME": os.getenv("OS_NAME", "auto"),
    "SHELL_NAME": os.getenv("SHELL_NAME", "auto"),
    # New features might add their own config variables here.
}


class Config(dict):  # type: ignore
    """Config reader/writer.

    IMPORTANT: importing this project (tests, IDE, type-checkers) must not
    create config files or prompt for keys.
    """

    def __init__(self, config_path: Path, *, create_if_missing: bool = False, **defaults: Any):
        self.config_path = config_path

        # Start with defaults.
        super().__init__(**defaults)

        # Overlay config file if it exists.
        if self._exists:
            self._read()

        # Optionally persist (CLI runtime can opt into this).
        if create_if_missing and not self._exists:
            self.ensure_created()

    @property
    def _exists(self) -> bool:
        return self.config_path.exists()

    def ensure_created(self) -> None:
        """Create parent dirs + write config file (if possible)."""

        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._write()

    def _write(self) -> None:
        try:
            with open(self.config_path, "w", encoding="utf-8") as file:
                string_config = ""
                for key, value in self.items():
                    string_config += f"{key}={value}\n"
                file.write(string_config)
        except PermissionError:
            # If we can't write to the config file, just skip it.
            pass

    def _read(self) -> None:
        with open(self.config_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    self[key] = value

    def get_optional(self, key: str, default: str | None = None) -> str | None:
        """Return config value or default (never raises).

        Environment variables override config-file values.
        """

        value = os.getenv(key) or super().get(key)
        return value if value not in (None, "") else default

    def get_required(self, key: str) -> str:
        value = self.get_optional(key)
        if value is None:
            raise UsageError(f"Missing config key: {key}")
        return value

    # Back-compat: existing code uses cfg.get(...). Keep strict behavior.
    def get(self, key: str) -> str:  # type: ignore
        return self.get_required(key)


# Global singleton (read-only by default; CLI can call cfg.ensure_created()).
cfg = Config(SHELL_GPT_CONFIG_PATH, create_if_missing=False, **DEFAULT_CONFIG)

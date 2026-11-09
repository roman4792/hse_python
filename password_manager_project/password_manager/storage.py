"""JSON persistence; file paths come from environment variables."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, cast

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)


class JSONStorage:
    """Read and write one JSON file named by an env var."""

    def __init__(self, env_key: str) -> None:
        env_filename = os.getenv(env_key)

        if not env_filename:
            raise KeyError(
                f"ошибка конфигурации: переменная окружения {env_key} не задана в .env файле. "
                f"Добавьте в .env строку вида {env_key}=your_file.json"
            )

        self.filename = BASE_DIR / env_filename

    def load(self) -> dict[str, Any]:
        """Load a dict from disk; missing file yields an empty dict."""
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    return {}
                return cast(Dict[str, Any], data)
        except FileNotFoundError:
            return {}
        except OSError as e:
            print(f"КРИТИЧЕСКАЯ ОШИБКА: Не удалось прочитать файл базы данных: {e}")
            return {}

    def save(self, data: dict[str, Any]) -> None:
        """Serialize dict to JSON."""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"Не удалось сохранить данные в файл: {e}")

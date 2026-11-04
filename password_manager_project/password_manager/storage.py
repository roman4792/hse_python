import json
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

class JSONStorage:
    def __init__(self, env_key: str):
        env_filename = os.getenv(env_key)

        if not env_filename:
            raise KeyError(
                f"ошибка конфигурации: переменная окружения {env_key} не задана в .env файле"
                f"добавьте в .env строку вида {env_key}=your_file.json"
            )

        self.filename = BASE_DIR / env_filename

    def load(self) -> dict:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"КРИТИЧЕСКАЯ ОШИБКА: Не удалось прочитать файл базы данных: {e}")
            return None

    def save(self, data: dict) -> None:
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Не удалось сохранить данные в файл: {e}")

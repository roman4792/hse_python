# Менеджер паролей (лаб. 1, трек DevOps, тема Б1)

Консольное приложение: мастер-пароль (PBKDF2 + соль), записи «сервис / логин / пароль» в JSON,
пароли записей шифруются через `cryptography` (Fernet). Соответствует **части 0** (общие требования)
и **Б1** из задания курса.

## Что реализовано

| Требование (Б1) | Как сделано |
|-----------------|-------------|
| Мастер-пароль только как хэш | PBKDF2-HMAC-SHA256, случайная соль в `auth.json` |
| `add` / `list` / `get` / `delete` | Интерактивное меню после `--unlock` |
| Скрытый ввод | `getpass` |
| CLI `--init` / `--unlock` | `password_manager.py` или `uv run python password_manager.py` |
| `_load` / `_persist` | `PasswordManager._load`, `_persist` + `JSONStorage` |
| Генератор `--generate` (Б1.5) | `generate_password`, буквы, цифры, спецсимволы |
| Шифрование записей (Б1.5) | Fernet, ключ из мастер-пароля |

## Установка

Нужен [uv](https://docs.astral.sh/uv/):

```bash
cd password_manager_project
uv sync
```

Скопируй `.env.example` в `.env` (имена файлов хранилища). `.env` и `*.json` в `.gitignore`.

## Запуск

```bash
uv run python password_manager.py --init
uv run python password_manager.py --unlock
uv run python password_manager.py --generate
uv run python password_manager.py --generate 24
```

После `--unlock`: команды `add`, `list`, `get`, `delete`, `exit`.

## Тесты и качество (часть 0)

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict password_manager tests
uv run mypy --strict --follow-imports=skip password_manager.py
```

На каждый push в GitHub Actions: `pytest`, `ruff`, `mypy` (см. `../.github/workflows/ci.yml`).

Тесты покрывают пункты **Б1.4** (unlock, init один раз, add/list/get, delete, нет plaintext на диске)
и генератор (**Б1.5**).

## Структура (пакет + tests, п. 0.1)

```
password_manager_project/
├── password_manager.py      # точка входа для задания (тонкий launcher)
├── password_manager/
│   ├── cli.py               # argparse и меню (без «простыни» в main)
│   ├── manager.py           # PasswordManager, generate_password
│   └── storage.py           # JSONStorage
├── tests/
│   └── test_manager.py
├── pyproject.toml
└── .env.example
```

## API `PasswordManager` (Б1.3)

- `init_master(password)` — создать хэш мастера  
- `unlock(password) -> bool`  
- `add_entry(name, login, pwd)`  
- `list_entries() -> list[str]`  
- `get_entry(name)`  
- `delete_entry(name)`  
- `_load()` / `_persist()` — внутреннее сохранение

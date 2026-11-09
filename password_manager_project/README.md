# Менеджер паролей

Консольное приложение для хранения паролей. Вход по мастер-паролю, записи
(сервис, логин, пароль) лежат в JSON-файле, сами пароли хранятся в зашифрованном виде.

## Что умеет

- создание мастер-пароля (`--init`): хранится только хэш PBKDF2-SHA256 со случайной солью;
- вход по мастер-паролю (`--unlock`), ввод скрыт через `getpass`;
- меню: `add` (добавить), `list` (названия без паролей), `get` (показать пароль после повторного ввода мастер-пароля), `delete` (удалить), `exit`;
- шифрование паролей в записях через `cryptography` (Fernet), ключ получается из мастер-пароля и не хранится;
- генератор надёжных паролей (`--generate`): буквы двух регистров, цифры, спецсимволы.

## Установка

Нужен [uv](https://docs.astral.sh/uv/):

```bash
brew install uv
cd password_manager_project
uv sync
```

## Настройка

Создай в папке `password_manager_project` файл `.env` с именами файлов хранилища:

```
FILE_NAME=passwords.json
AUTH_FILE_NAME=auth.json
```

`FILE_NAME` - записи с паролями, `AUTH_FILE_NAME` - хэш и соли мастер-пароля.
Файл `.env` и все `*.json` добавлены в `.gitignore`, в репозиторий они не попадают.

## Запуск

```bash
uv run python password_manager.py --init       # создать мастер-пароль
uv run python password_manager.py --unlock     # войти, дальше меню
uv run python password_manager.py --generate   # сгенерировать пароль (16 символов)
uv run python password_manager.py --generate 24
```

Повторный `--init` ничего не перезаписывает: мастер-пароль уже создан.

## Тесты

```bash
uv run pytest
```

Тесты работают во временных файлах, настоящие `auth.json` и `passwords.json` не затрагиваются.
Они проверяют:

- `unlock` с верным и неверным паролем;
- что мастер-пароль нельзя создать второй раз;
- цепочку `add` -> `list` -> `get`;
- `delete`;
- что в файлах нет мастер-пароля и паролей записей в открытом виде.

Проверка стиля:

```bash
uv run ruff check .
uv run ruff format --check .
```

Тесты и `ruff` запускаются в GitHub Actions на каждый push (`.github/workflows/ci.yml`).

## Структура

```
password_manager_project/
├── password_manager.py        # CLI: argparse и меню
├── password_manager/
│   ├── manager.py             # PasswordManager, generate_password
│   └── storage.py             # JSONStorage: чтение и запись JSON
├── tests/
│   └── test_manager.py
└── pyproject.toml
```

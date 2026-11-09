import argparse
import getpass

from password_manager.manager import PasswordManager, generate_password


def ask_new_master() -> str:
    while True:
        pwd1 = getpass.getpass("Придумайте мастер-пароль: ")
        pwd2 = getpass.getpass("Повторите пароль: ")
        if not pwd1:
            print("Пароль не может быть пустым")
        elif pwd1 != pwd2:
            print("Пароли не совпадают")
        else:
            return pwd1


def do_init(manager: PasswordManager) -> None:
    try:
        manager.init_master(ask_new_master())
    except PermissionError as e:
        print(e)
        return
    print("Мастер-пароль создан. Теперь запустите с --unlock")


def do_unlock(manager: PasswordManager) -> bool:
    if manager.master_hash is None:
        print("Сначала создайте мастер-пароль: python password_manager.py --init")
        return False

    password = getpass.getpass("Мастер-пароль: ")
    if manager.unlock(password):
        return True
    print("Неверный мастер-пароль")
    return False


def handle_add(manager: PasswordManager) -> None:
    name = input("Название сервиса: ")
    login = input("Логин: ")
    pwd = getpass.getpass("Пароль (Enter - сгенерировать): ")
    if not pwd:
        pwd = generate_password()
        print("Сгенерирован пароль:", pwd)
    manager.add_entry(name, login, pwd)
    print("Запись добавлена")


def handle_list(manager: PasswordManager) -> None:
    names = manager.list_entries()
    if not names:
        print("Записей пока нет")
    for name in names:
        print("-", name)


def handle_get(manager: PasswordManager) -> None:
    name = input("Название сервиса: ")

    password = getpass.getpass("Подтвердите мастер-пароль: ")
    if not manager.unlock(password):
        print("Неверный мастер-пароль")
        return

    entry = manager.get_entry(name)
    if entry is None:
        print("Такой записи нет")
        return
    print("Логин:", entry["login"])
    print("Пароль:", entry["pwd"])


def handle_delete(manager: PasswordManager) -> None:
    name = input("Название сервиса: ")
    if name in manager.list_entries():
        manager.delete_entry(name)
        print("Запись удалена")
    else:
        print("Такой записи нет")


def run_menu(manager: PasswordManager) -> None:
    actions = {
        "add": handle_add,
        "list": handle_list,
        "get": handle_get,
        "delete": handle_delete,
    }
    while True:
        command = input("\nadd / list / get / delete / exit > ").strip().lower()
        if command == "exit":
            break
        if command in actions:
            actions[command](manager)
        else:
            print("Неизвестная команда")


def main() -> None:
    parser = argparse.ArgumentParser(description="Менеджер паролей")
    parser.add_argument("--init", action="store_true", help="создать мастер-пароль")
    parser.add_argument("--unlock", action="store_true", help="войти в менеджер")
    parser.add_argument(
        "--generate",
        nargs="?",
        const=16,
        type=int,
        metavar="LEN",
        help="сгенерировать пароль (длина по умолчанию 16)",
    )
    args = parser.parse_args()

    if args.generate is not None:
        try:
            print(generate_password(args.generate))
        except ValueError as e:
            print(e)
        return

    if not args.init and not args.unlock:
        parser.print_help()
        return

    try:
        manager = PasswordManager()
    except KeyError as e:
        print(e)
        return

    if args.init:
        do_init(manager)
    elif do_unlock(manager):
        run_menu(manager)


if __name__ == "__main__":
    main()

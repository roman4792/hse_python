from storage import JSONStorage

class PasswordManager:
    def __init__(self):
        self.master_hash = None
        self.entries = {}
        self.is_unlocked = False

    def init_master(self, password: str):
        # Логика создания мастер-пароля (например, хэширование)
        pass

    def unlock(self, password: str) -> bool:
        # Проверка пароля
        return True

    def add_entry(self, name: str, login: str, pwd: str):
        if not self.is_unlocked:
            raise PermissionError("Сначала разблокируйте менеджер!")
        self.entries[name] = {"login": login, "pwd": pwd}
        self._persist()

    def list_entries(self) -> list[str]:
        return list(self.entries.keys())

    def get_entry(self, name: str):
        return self.entries.get(name)

    def delete_entry(self, name: str):
        if name in self.entries:
            del self.entries[name]
            self._persist()

    def _persist(self):
        # Вызываем функцию сохранения из соседнего модуля
        save_to_json(self.entries)

    def _load(self):
        self.entries = load_from_json()

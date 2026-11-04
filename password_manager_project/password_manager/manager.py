from .storage import JSONStorage

class PasswordManager:
    def __init__(self):
        self.auth_storage = JSONStorage("AUTH_FILE_NAME")
        self.data_storage = JSONStorage("FILE_NAME")

        auth_data = self.auth_storage.load()
        self.master_hash = auth_data.get("master_hash")

        self.entries = self.data_storage.load()

        self.is_unlocked = False

    def init_master(self, password: str):
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
        if not self.is_unlocked:
            raise PermissionError("Сначала разблокируйте менеджер!")
        return list(self.entries.keys())

    def get_entry(self, name: str):
        if not self.is_unlocked:
            raise PermissionError("Сначала разблокируйте менеджер!")
        return self.entries.get(name)

    def delete_entry(self, name: str) -> None:
        if not self.is_unlocked:
            raise PermissionError("Сначала разблокируйте менеджер!")

        if name in self.entries:
            del self.entries[name]
            self._persist()

    def _persist(self) -> None:
        self.data_storage.save(self.entries)
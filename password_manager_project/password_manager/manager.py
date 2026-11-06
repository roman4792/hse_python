import hashlib
import os
from .storage import JSONStorage

class PasswordManager:
    def __init__(self):
        self.auth_storage = JSONStorage("AUTH_FILE_NAME")
        self.data_storage = JSONStorage("FILE_NAME")

        auth_data = self.auth_storage.load()
        self.master_hash = auth_data.get("master_hash")
        self.master_salt = auth_data.get("salt")

        self.entries = self.data_storage.load()

        self.is_unlocked = False

    def init_master(self, password: str) -> None:
        if self.master_hash is not None:
            raise PermissionError("Мастер-пароль уже создан!")

        salt = os.urandom(16)
        hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200000)

        self.master_salt = salt.hex()
        self.master_hash = hash_bytes.hex()
        self.auth_storage.save({"master_hash": self.master_hash, "salt": self.master_salt})

    def unlock(self, password: str) -> bool:
        if self.master_hash is None:
            return False

        salt = bytes.fromhex(self.master_salt)
        check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200000).hex()

        if check == self.master_hash:
            self.is_unlocked = True
            return True
        return False

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
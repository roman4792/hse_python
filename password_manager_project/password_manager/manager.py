from __future__ import annotations
import base64
import hashlib
import os
from cryptography.fernet import Fernet
from .storage import JSONStorage


class PasswordManager:
    def __init__(self):
        self.auth_storage = JSONStorage("AUTH_FILE_NAME")
        self.data_storage = JSONStorage("FILE_NAME")

        auth_data = self.auth_storage.load()
        self.master_hash = auth_data.get("master_hash")
        self.master_salt = auth_data.get("salt")
        self.enc_salt = auth_data.get("enc_salt")
        self.fernet = None

        self.entries = self.data_storage.load()

        self.is_unlocked = False

    def _make_fernet(self, password: str) -> Fernet:
        salt = bytes.fromhex(self.enc_salt)
        key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200000, dklen=32)
        return Fernet(base64.urlsafe_b64encode(key))

    def init_master(self, password: str) -> None:
        if self.master_hash is not None:
            raise PermissionError("Мастер-пароль уже создан!")

        salt = os.urandom(16)
        hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200000)

        self.master_salt = salt.hex()
        self.master_hash = hash_bytes.hex()
        self.enc_salt = os.urandom(16).hex()
        self.auth_storage.save({
            "master_hash": self.master_hash,
            "salt": self.master_salt,
            "enc_salt": self.enc_salt,
        })

    def unlock(self, password: str) -> bool:
        if self.master_hash is None:
            return False

        salt = bytes.fromhex(self.master_salt)
        check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200000).hex()

        if check == self.master_hash:
            self.is_unlocked = True
            self.fernet = self._make_fernet(password)
            return True
        return False

    def add_entry(self, name: str, login: str, pwd: str):
        if not self.is_unlocked:
            raise PermissionError("Сначала разблокируйте менеджер!")

        encrypted = self.fernet.encrypt(pwd.encode()).decode()
        self.entries[name] = {"login": login, "pwd": encrypted}
        self._persist()

    def list_entries(self) -> list[str]:
        if not self.is_unlocked:
            raise PermissionError("Сначала разблокируйте менеджер!")
        return list(self.entries.keys())

    def get_entry(self, name: str):
        if not self.is_unlocked:
            raise PermissionError("Сначала разблокируйте менеджер!")

        entry = self.entries.get(name)
        if entry is None:
            return None

        pwd = self.fernet.decrypt(entry["pwd"].encode()).decode()
        return {"login": entry["login"], "pwd": pwd}

    def delete_entry(self, name: str) -> None:
        if not self.is_unlocked:
            raise PermissionError("Сначала разблокируйте менеджер!")

        if name in self.entries:
            del self.entries[name]
            self._persist()

    def _persist(self) -> None:
        self.data_storage.save(self.entries)
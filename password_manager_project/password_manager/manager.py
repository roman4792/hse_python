"""PasswordManager: master hash (PBKDF2), Fernet-backed entry storage."""

from __future__ import annotations

import base64
import hashlib
import os
import random
import secrets
import string
from typing import Dict, cast

from cryptography.fernet import Fernet

from .storage import JSONStorage


class PasswordManager:
    """In-memory vault; entry passwords are encrypted on disk."""

    def __init__(self) -> None:
        self.auth_storage = JSONStorage("AUTH_FILE_NAME")
        self.data_storage = JSONStorage("FILE_NAME")

        self.master_hash: str | None = None
        self.master_salt: str | None = None
        self.enc_salt: str | None = None
        self.fernet: Fernet | None = None
        self.entries: dict[str, dict[str, str]] = {}

        self._load()

        self.is_unlocked = False

    def _load(self) -> None:
        """Read master auth metadata and entries from JSON files."""
        auth_data = self.auth_storage.load()
        self.master_hash = auth_data.get("master_hash")
        self.master_salt = auth_data.get("salt")
        self.enc_salt = auth_data.get("enc_salt")

        self.entries = cast(Dict[str, Dict[str, str]], self.data_storage.load())

    def _make_fernet(self, password: str) -> Fernet:
        """Derive a Fernet key from the master password and per-vault salt."""
        if self.enc_salt is None:
            raise RuntimeError("Encryption salt is missing")
        salt = bytes.fromhex(self.enc_salt)
        key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200000, dklen=32)
        return Fernet(base64.urlsafe_b64encode(key))

    def init_master(self, password: str) -> None:
        """Create master password hash and salts (one-time setup)."""
        if self.master_hash is not None:
            raise PermissionError("Мастер-пароль уже создан!")

        salt = os.urandom(16)
        hash_bytes = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200000)

        self.master_salt = salt.hex()
        self.master_hash = hash_bytes.hex()
        self.enc_salt = os.urandom(16).hex()
        self.auth_storage.save(
            {
                "master_hash": self.master_hash,
                "salt": self.master_salt,
                "enc_salt": self.enc_salt,
            }
        )

    def unlock(self, password: str) -> bool:
        """Verify master password and prepare Fernet for entry passwords."""
        if self.master_hash is None or self.master_salt is None:
            return False

        salt = bytes.fromhex(self.master_salt)
        check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200000).hex()

        if check == self.master_hash:
            self.is_unlocked = True
            self.fernet = self._make_fernet(password)
            return True
        return False

    def add_entry(self, name: str, login: str, pwd: str) -> None:
        """Add or replace a service entry."""
        if not self.is_unlocked:
            raise PermissionError("Сначала разблокируйте менеджер!")

        fernet = self.fernet
        if fernet is None:
            raise RuntimeError("Encryption is not initialized")

        encrypted = fernet.encrypt(pwd.encode()).decode()
        self.entries[name] = {"login": login, "pwd": encrypted}
        self._persist()

    def list_entries(self) -> list[str]:
        """Return service names (no passwords)."""
        if not self.is_unlocked:
            raise PermissionError("Сначала разблокируйте менеджер!")
        return list(self.entries.keys())

    def get_entry(self, name: str) -> dict[str, str] | None:
        """Return login and decrypted password, or None if missing."""
        if not self.is_unlocked:
            raise PermissionError("Сначала разблокируйте менеджер!")

        fernet = self.fernet
        if fernet is None:
            raise RuntimeError("Encryption is not initialized")

        entry = self.entries.get(name)
        if entry is None:
            return None

        pwd = fernet.decrypt(entry["pwd"].encode()).decode()
        return {"login": entry["login"], "pwd": pwd}

    def delete_entry(self, name: str) -> None:
        """Remove an entry by service name."""
        if not self.is_unlocked:
            raise PermissionError("Сначала разблокируйте менеджер!")

        if name in self.entries:
            del self.entries[name]
            self._persist()

    def _persist(self) -> None:
        """Write entries to the data JSON file."""
        self.data_storage.save(self.entries)


def generate_password(length: int = 16) -> str:
    """Random password with lower, upper, digit, and punctuation."""
    if length < 4:
        raise ValueError("Длина пароля должна быть не меньше 4")

    groups = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        string.punctuation,
    ]

    chars = [secrets.choice(group) for group in groups]

    all_chars = "".join(groups)
    while len(chars) < length:
        chars.append(secrets.choice(all_chars))

    random.SystemRandom().shuffle(chars)
    return "".join(chars)

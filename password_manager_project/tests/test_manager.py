"""Tests for PasswordManager"""

import json
import re
from pathlib import Path

import pytest

from password_manager.manager import PasswordManager, generate_password


@pytest.fixture
def manager(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> PasswordManager:
    """Vault with master password already initialized."""
    monkeypatch.setenv("AUTH_FILE_NAME", str(tmp_path / "auth.json"))
    monkeypatch.setenv("FILE_NAME", str(tmp_path / "data.json"))

    m = PasswordManager()
    m.init_master("master123")
    return m


def test_unlock(manager: PasswordManager) -> None:
    """Correct master password unlocks; wrong password does not."""
    assert manager.unlock("master123") is True
    assert manager.unlock("master1234") is False


def test_init_master_only_once(manager: PasswordManager) -> None:
    """Second init_master must not overwrite the master hash."""
    old_hash = manager.master_hash

    second = PasswordManager()
    with pytest.raises(PermissionError):
        second.init_master("another")

    assert second.master_hash == old_hash


def test_add_list_get(manager: PasswordManager) -> None:
    """add -> list shows name; get returns login and password."""
    manager.unlock("master123")
    manager.add_entry("github", "roman", "secret")

    assert manager.list_entries() == ["github"]
    assert manager.get_entry("github") == {"login": "roman", "pwd": "secret"}


def test_delete(manager: PasswordManager) -> None:
    """delete removes the entry from the vault."""
    manager.unlock("master123")
    manager.add_entry("github", "roman", "secret")
    manager.delete_entry("github")

    assert manager.list_entries() == []
    assert manager.get_entry("github") is None


def test_nothing_stored_in_plain_text(manager: PasswordManager, tmp_path: Path) -> None:
    """Master and entry passwords must not appear as plaintext on disk."""
    manager.unlock("master123")
    manager.add_entry("github", "roman", "secret")

    auth_text = (tmp_path / "auth.json").read_text(encoding="utf-8")
    data_text = (tmp_path / "data.json").read_text(encoding="utf-8")

    assert "master123" not in auth_text
    assert "secret" not in data_text

    saved = json.loads(data_text)
    assert saved["github"]["pwd"] != "secret"


def test_generate_password_length_and_charset() -> None:
    """B1.5: generator uses letters, digits, and punctuation."""
    pwd = generate_password(20)
    assert len(pwd) == 20
    assert re.search(r"[a-z]", pwd)
    assert re.search(r"[A-Z]", pwd)
    assert re.search(r"\d", pwd)
    assert re.search(r"[^\w]", pwd)


def test_generate_password_too_short() -> None:
    with pytest.raises(ValueError):
        generate_password(3)

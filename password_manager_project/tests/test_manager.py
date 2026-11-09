import json
from pathlib import Path

import pytest

from password_manager.manager import PasswordManager


@pytest.fixture
def manager(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> PasswordManager:
    monkeypatch.setenv("AUTH_FILE_NAME", str(tmp_path / "auth.json"))
    monkeypatch.setenv("FILE_NAME", str(tmp_path / "data.json"))

    m = PasswordManager()
    m.init_master("master123")
    return m


def test_unlock(manager: PasswordManager) -> None:
    assert manager.unlock("master123") is True
    assert manager.unlock("master1234") is False


def test_init_master_only_once(manager: PasswordManager) -> None:
    old_hash = manager.master_hash

    second = PasswordManager()
    with pytest.raises(PermissionError):
        second.init_master("another")

    assert second.master_hash == old_hash


def test_add_list_get(manager: PasswordManager) -> None:
    manager.unlock("master123")
    manager.add_entry("github", "roman", "secret")

    assert manager.list_entries() == ["github"]
    assert manager.get_entry("github") == {"login": "roman", "pwd": "secret"}


def test_delete(manager: PasswordManager) -> None:
    manager.unlock("master123")
    manager.add_entry("github", "roman", "secret")
    manager.delete_entry("github")

    assert manager.list_entries() == []
    assert manager.get_entry("github") is None


def test_nothing_stored_in_plain_text(manager: PasswordManager, tmp_path: Path) -> None:
    manager.unlock("master123")
    manager.add_entry("github", "roman", "secret")

    auth_text = (tmp_path / "auth.json").read_text(encoding="utf-8")
    data_text = (tmp_path / "data.json").read_text(encoding="utf-8")

    assert "master123" not in auth_text
    assert "secret" not in data_text

    saved = json.loads(data_text)
    assert saved["github"]["pwd"] != "secret"

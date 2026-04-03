from app.config import Settings


def test_settings_uses_database_path_from_env(monkeypatch, tmp_path):
    database_path = tmp_path / "custom.db"
    monkeypatch.setenv("DATABASE_PATH", str(database_path))

    settings = Settings()

    assert settings.database_path == database_path

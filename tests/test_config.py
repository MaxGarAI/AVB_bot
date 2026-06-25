from app.config import Settings


def test_settings_defaults_use_sqlite_and_free_openrouter_model():
    settings = Settings(openrouter_api_key="test-key")

    assert settings.database_url.endswith("databaseAVB.db")
    assert settings.openrouter_model == "meta-llama/llama-3.1-8b-instruct:free"
    assert settings.app_env == "dev"

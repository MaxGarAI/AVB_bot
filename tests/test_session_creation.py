from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_session_returns_token_and_chat_url():
    response = client.post(
        "/api/sessions",
        json={
            "sales_manager_name": "Ivan",
            "source_campaign": "manual-outreach",
            "custom_prompt_instructions": "Спроси про аудиторию и сезонность.",
        },
    )

    assert response.status_code == 201
    data = response.json()

    assert data["session_token"]
    assert data["chat_url"].endswith(f"/chat/{data['session_token']}")
    assert data["status"] == "created"
    assert data["current_stage"] == "INIT"

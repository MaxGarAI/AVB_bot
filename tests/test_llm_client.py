from app.services.llm_client import OpenRouterClient, OpenRouterClientError


def test_client_raises_error_when_api_key_is_empty():
    try:
        OpenRouterClient(api_key="")
    except OpenRouterClientError as exc:
        assert "API key" in str(exc)
    else:
        raise AssertionError("Expected OpenRouterClientError")


def test_client_builds_request_with_openrouter_model():
    client = OpenRouterClient(api_key="test-key")
    payload = client._build_payload(
        messages=[{"role": "user", "content": "Привет"}],
        temperature=0.3,
    )

    assert payload["model"] == client.model
    assert payload["messages"] == [{"role": "user", "content": "Привет"}]
    assert payload["temperature"] == 0.3


def test_client_returns_mocked_response_for_valid_call():
    import json
    from unittest.mock import patch

    class FakeResponse:
        status_code = 200

        def json(self):
            return {
                "choices": [
                    {"message": {"content": json.dumps({"answer": "ok"})}}
                ]
            }

    client = OpenRouterClient(api_key="test-key")
    with patch("httpx.Client.post", return_value=FakeResponse()):
        result = client.chat_completion(messages=[{"role": "user", "content": "test"}])

    assert result == json.dumps({"answer": "ok"})
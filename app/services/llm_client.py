from __future__ import annotations

import httpx

from app.config import get_settings


class OpenRouterClientError(RuntimeError):
    pass


class OpenRouterClient:
    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: str | None = None) -> None:
        settings = get_settings()
        self._api_key = api_key if api_key is not None else settings.openrouter_api_key
        self.model = settings.openrouter_model
        if not self._api_key or not self._api_key.strip():
            raise OpenRouterClientError("OpenRouter API key is required")

    def chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.3,
        timeout: float = 60.0,
    ) -> str:
        payload = self._build_payload(messages, temperature)
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                self.BASE_URL,
                json=payload,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
            )
            if response.status_code != 200:
                raise OpenRouterClientError(
                    f"OpenRouter returned {response.status_code}: {response.text[:500]}"
                )
            body = response.json()
        return body["choices"][0]["message"]["content"]

    def _build_payload(self, messages: list[dict[str, str]], temperature: float) -> dict:
        return {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
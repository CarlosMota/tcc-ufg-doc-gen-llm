from typing import Optional

import httpx

from ...domain.llm import LLMClient, LLMRequest, LLMResponse


class _OpenAICompatibleBase(LLMClient):
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str],
        model: Optional[str],
        timeout: float,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def generate(self, request: LLMRequest) -> LLMResponse:
        if not request.model and not self.model:
            raise ValueError("Modelo não informado para o LLM.")

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload: dict = {
            "model": request.model or self.model,
            "messages": [{"role": "user", "content": request.prompt}],
            "temperature": request.temperature,
        }
        if request.max_tokens:
            payload["max_tokens"] = request.max_tokens

        with httpx.Client(base_url=self.base_url, timeout=self.timeout) as client:
            response = client.post("/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        choices = data.get("choices") or []
        message = choices[0].get("message") if choices else {}
        text = message.get("content") if message else None
        if not text:
            raise ValueError("Resposta vazia do LLM.")
        return LLMResponse(text=text, raw=data)

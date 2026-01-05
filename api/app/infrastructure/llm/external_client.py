from typing import Optional

from ._openai_compatible import _OpenAICompatibleBase


class ExternalLLMClient(_OpenAICompatibleBase):
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        if not api_key:
            raise ValueError("API key obrigatória para provedor externo.")
        super().__init__(
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout=timeout,
        )

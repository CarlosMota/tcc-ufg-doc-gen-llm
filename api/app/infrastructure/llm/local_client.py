from typing import Optional

from ._openai_compatible import _OpenAICompatibleBase


class LocalLLMClient(_OpenAICompatibleBase):
    def __init__(
        self,
        base_url: str,
        model: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        super().__init__(
            base_url=base_url,
            api_key=None,
            model=model,
            timeout=timeout,
        )

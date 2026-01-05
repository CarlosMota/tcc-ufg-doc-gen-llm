from typing import Optional

from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    prompt: str = Field(..., description="Prompt completo enviado ao modelo.")
    model: Optional[str] = Field(None, description="Modelo a ser usado na chamada.")
    temperature: float = Field(0.2, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, ge=1)


class LLMResponse(BaseModel):
    text: str
    raw: Optional[dict] = None

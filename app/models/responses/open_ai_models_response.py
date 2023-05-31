from dataclasses import dataclass

from app.models.open_ai_model import OpenAiModel


@dataclass
class OpenAiModelsResponse:
    object: str
    data: list[OpenAiModel]
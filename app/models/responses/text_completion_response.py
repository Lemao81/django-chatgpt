from dataclasses import dataclass

from openai.openai_object import OpenAIObject

from app.models.dtos.text_completion_choice import TextCompletionChoice


@dataclass
class TextCompletionResponse:
    def __init__(self, open_ai_object: OpenAIObject):
        choices: list[OpenAIObject] = open_ai_object.get('choices')
        self.choices: list[TextCompletionChoice] = list(map(lambda o: TextCompletionChoice(o), choices))

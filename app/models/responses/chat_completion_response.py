from dataclasses import dataclass

from openai.openai_object import OpenAIObject

from app.models.dtos.chat_completion_choice import ChatCompletionChoice


@dataclass()
class ChatCompletionResponse:
    def __init__(self, open_ai_object: OpenAIObject):
        choices: list[OpenAIObject] = open_ai_object.get('choices')
        self.choices: list[ChatCompletionChoice] = list(map(lambda o: ChatCompletionChoice(o), choices))

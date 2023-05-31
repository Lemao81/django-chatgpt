from openai.openai_object import OpenAIObject

from app.models.dtos.chat_completion_message import ChatCompletionMessage


class ChatCompletionChoice:
    def __init__(self, open_ai_object: OpenAIObject):
        self.index: int = open_ai_object.get('index')
        self.message: ChatCompletionMessage = ChatCompletionMessage(open_ai_object.get('message'))
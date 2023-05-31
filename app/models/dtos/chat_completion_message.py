from openai.openai_object import OpenAIObject


class ChatCompletionMessage:
    def __init__(self,  open_ai_object: OpenAIObject):
        self.role: str = open_ai_object.get('role')
        self.content: str = open_ai_object.get('content')
from openai.openai_object import OpenAIObject


class TextCompletionChoice:
    def __init__(self, open_ai_object: OpenAIObject):
        self.text: str = open_ai_object.get('text')

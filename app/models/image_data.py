from openai.openai_object import OpenAIObject


class ImageData:
    def __init__(self, open_ai_object: OpenAIObject):
        self.url: str = open_ai_object.get('url')

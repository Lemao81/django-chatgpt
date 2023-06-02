from dataclasses import dataclass

from openai.openai_object import OpenAIObject

from app.models.image_data import ImageData


@dataclass()
class ImageCreationResponse:
    def __init__(self, open_ai_object: OpenAIObject):
        datas: list[OpenAIObject] = open_ai_object.get('data')
        self.data: list[ImageData] = list(map(lambda x: ImageData(x), datas))

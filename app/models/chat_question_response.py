from app.models.chat_message import ChatMessage


class ChatQuestionResponse:
    def __init__(self, question: ChatMessage, response: ChatMessage):
        self.question: ChatMessage = question
        self.response: ChatMessage = response

    def get_chat_messages(self) -> list[ChatMessage]:
        return [ChatMessage(self.question.role, self.question.content), ChatMessage(self.response.role, self.response.content)]

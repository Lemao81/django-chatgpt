import os
import openai

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from openai.error import RateLimitError
from openai.openai_object import OpenAIObject
from rest_framework.exceptions import MethodNotAllowed

from .constants import AI_MODEL_TEXT_DAVINCI, AI_MODEL_GPT35, HTTP_GET, HTTP_POST, ROLE_USER, ROLE_ASSISTANT
from .models.chat_question_response import ChatQuestionResponse
from .models.chat_message import ChatMessage
from .models.forms.prompt_form import PromptForm
from .models.open_ai_model import OpenAiModel
from .models.responses.chat_completion_response import ChatCompletionResponse
from .models.responses.image_creation_response import ImageCreationResponse
from .models.responses.open_ai_models_response import OpenAiModelsResponse
from .models.responses.text_completion_response import TextCompletionResponse

_chat_question_responses: list[ChatQuestionResponse] = []


def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'app/home.html', {'title': 'Home'})


def qanda(request: HttpRequest) -> HttpResponse:
    form = PromptForm()
    answer = ''

    if request.method == HTTP_GET:
        pass
    elif request.method == HTTP_POST:
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            _set_api_key()
            try:
                response_object: OpenAIObject = openai.Completion.create(
                    model=AI_MODEL_TEXT_DAVINCI,
                    prompt=prompt,
                    max_tokens=100,
                    temperature=0
                )
                print(response_object)
                response = TextCompletionResponse(response_object)
                answer = response.choices[0].text
            except RateLimitError:
                answer = 'Rate limit error occurred'
    else:
        raise MethodNotAllowed

    context = {
        'title': 'Q and A',
        'form': form,
        'answer': answer
    }

    return render(request, 'app/qanda.html', context)


def chat(request: HttpRequest) -> HttpResponse:
    error = ''
    form = PromptForm()

    if request.method == HTTP_GET:
        pass
    elif request.method == HTTP_POST and 'reset_button' in request.POST:
        _chat_question_responses.clear()
    elif request.method == HTTP_POST:
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            chat_message_pairs = map(lambda x: x.get_chat_messages(), _chat_question_responses)
            chat_messages = [x for sublist in chat_message_pairs for x in sublist]
            messages = list(map(lambda x: {'role': x.role, 'content': x.content}, chat_messages))
            messages.append({'role': ROLE_USER, 'content': prompt})

            _set_api_key()
            try:
                response_object: OpenAIObject = openai.ChatCompletion.create(
                    model=AI_MODEL_GPT35,
                    messages=messages,
                    max_tokens=100,
                    temperature=0
                )
                print(response_object)
                response = ChatCompletionResponse(response_object)
                answer = response.choices[0].message.content
                _chat_question_responses.append(ChatQuestionResponse(ChatMessage(ROLE_USER, prompt), ChatMessage(ROLE_ASSISTANT, answer)))
                form = PromptForm()
            except RateLimitError:
                error = 'Rate limit error occurred'
    else:
        raise MethodNotAllowed

    context = {
        'title': 'Chat',
        'form': form,
        'question_responses': _chat_question_responses,
        'error': error
    }

    return render(request, 'app/chat.html', context)


def image(request: HttpRequest) -> HttpResponse:
    form = PromptForm()
    url = ''
    error = ''

    if request.method == HTTP_GET:
        pass
    elif request.method == HTTP_POST:
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            _set_api_key()
            try:
                response_object: OpenAIObject = openai.Image.create(
                    prompt=prompt,
                    size='1024x1024'
                )
                print(response_object)
                response = ImageCreationResponse(response_object)
                url = response.data[0].url
            except RateLimitError:
                error = 'Rate limit error occurred'
    else:
        raise MethodNotAllowed

    context = {
        'title': 'Image',
        'form': form,
        'url': url,
        'error': error
    }

    return render(request, 'app/image.html', context)


def _get_model_list() -> list[OpenAiModel]:
    response_object: OpenAIObject = openai.Model.list()
    response = OpenAiModelsResponse(**response_object.to_dict())
    return response.data


def _set_api_key():
    openai.api_key = _get_api_key()


def _get_api_key() -> str:
    return os.getenv('API_KEY')

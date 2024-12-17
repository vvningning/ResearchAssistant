from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.llms.chatglm import ChatGLM
from langchain_core.messages import ChatMessage
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatSparkLLM


def chat(request):
    response = {}
    question = request.GET.get('question')
    print(question)
    response['ans'] = "This is an answer."
    return JsonResponse(response)

# @csrf_exempt 如果是post加个这个

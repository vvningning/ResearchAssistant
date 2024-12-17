from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def chat(request):
    response = {}
    question = request.GET.get('question')
    print(question)
    response['ans'] = "This is an answer."
    return JsonResponse(response)


# @csrf_exempt 如果是post加个这个

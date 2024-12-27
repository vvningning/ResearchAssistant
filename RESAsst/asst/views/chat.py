from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pymilvus import connections, Collection

from asst.services.Embedding import get_embq_embedding, parser_Message
from asst.services.SparkChat import get_ans


def chat(request):
    response = {}
    question = request.GET.get('question')
    print(question)
    top_k = 3
    retrieval = retriever_qa(question, top_k)
    prompt = f'基于下面给出的资料，回答问题。基于下面给出的资料，回答问题。如果资料不足，回答不了，就回复不知道，下面是资料。\n'
    for idx, content in enumerate(retrieval):
        prompt += f'{idx + 1}. {content}\n'
    prompt += f'下面是问题:{question}'
    print(prompt)
    response['ans'] = get_ans(prompt)
    return JsonResponse(response)


def retriever_qa(query, top_k):
    connections.connect("default", host="localhost", port="19530")
    collection = Collection("asst")
    collection.load()
    search_params = {
        "metric_type": "COSINE",
        "params": {"nprobe": 10}
    }

    # fields = [
    #     FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    #     FieldSchema(name="user_id", dtype=DataType.INT64),
    #     FieldSchema(name="file_id", dtype=DataType.INT64),
    #     FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
    #     FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=2560),
    # ]

    APPID = '9b60d12e'
    APISecret = 'ZTUwYzNlZGNjMDhmNGQ5NDVjYThiZGEy'
    APIKEY = 'c3bb38b3fc5fdc87ad9b1bc670c3e2e9'
    res = get_embq_embedding(text=query, appid=APPID, apikey=APIKEY, apisecret=APISecret)
    query_vector = parser_Message(res)
    results = collection.search(
        data=[query_vector],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["content"]
    )

    retrieval = []
    for result in results[0]:
        print(f"Content: {result.entity.get('content')}, Similarity score: {result.score}")
        retrieval.append(result.entity.get('content'))

    print(retrieval)
    return retrieval

# @csrf_exempt 如果是post加个这个

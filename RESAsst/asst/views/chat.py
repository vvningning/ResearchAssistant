import langid
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import connections, Collection

from asst.services.Embedding import get_embq_embedding, parser_Message, get_embp_embedding
from asst.services.SparkChat import get_ans

APPID = '9b60d12e'
APISecret = 'ZTUwYzNlZGNjMDhmNGQ5NDVjYThiZGEy'
APIKEY = 'c3bb38b3fc5fdc87ad9b1bc670c3e2e9'


def chat(request):
    response = {}
    question = request.GET.get('question')
    language = langid.classify(question)[0]
    top_k = 3
    retrieval = retriever_qa(question, top_k)
    prompt = f'Based on the following materials, answer the question. If the materials are insufficient, reply "I don’t know". Here are the materials:\n'
    if language == 'zh':
        prompt = f'基于下面给出的资料，回答问题。基于下面给出的资料，回答问题。如果资料不足，回答不了，就回复不知道，下面是资料。\n'
    for idx, content in enumerate(retrieval):
        prompt += f'{idx + 1}. {content}\n'
    if language == 'zh':
        prompt += f'下面是问题：{question}'
    else:
        prompt += f'Here are the question:{question}'
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


# 向量数据库插入
def insert_collection(paper_id, content):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=40,
        length_function=len
    )
    split_docs = text_splitter.create_documents([content])
    collection = Collection("paper_collection")
    collection.load()
    for document in split_docs:
        res = get_embp_embedding(document.page_content, appid=APPID, apikey=APIKEY, apisecret=APISecret)
        vector = parser_Message(res)
        collection.insert([{"paper_id": paper_id, "embedding": vector, "text": document.page_content}])

# @csrf_exempt 如果是post加个这个

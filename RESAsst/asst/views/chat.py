import json
import langid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import connections, Collection

from asst.models import ChatHistory
from asst.services.Embedding import get_embq_embedding, parser_Message, get_embp_embedding
from asst.services.SparkChat import get_ans, init_messages

APPID = '9b60d12e'
APISecret = 'ZTUwYzNlZGNjMDhmNGQ5NDVjYThiZGEy'
APIKEY = 'c3bb38b3fc5fdc87ad9b1bc670c3e2e9'


def chat(request):
    response = {}
    question = request.GET.get('question')
    paper_id = request.GET.get('paper_id')
    print(question, paper_id)
    language = langid.classify(question)[0]
    top_k = 5
    retrieval = retriever_qa(question, top_k, paper_id)
    prompt = f'Based on the following materials, answer the question. If the materials are insufficient, reply "I don\'t know". Here are the materials:\n'
    if language == 'zh':
        prompt = f'基于下面给出的资料，回答问题。如果资料不足，回答不了，就回复不知道，下面是资料：\n'
    for idx, content in enumerate(retrieval):
        prompt += f'{idx + 1}. {content}\n'
    if language == 'zh':
        prompt += f'下面是问题：{question}'
    else:
        prompt += f'Here are the question:{question}'
    print(prompt)
    response['ans'] = get_ans(request, prompt)
    user_log = ChatHistory(eid=paper_id, isUser=True, message=question)
    user_log.save()
    bot_log = ChatHistory(id=user_log.msgId+1, eid=paper_id, isUser=False, meseage=response['ans'])
    bot_log.save()
    return JsonResponse(response)


def retriever_qa(query, top_k, paper_id):
    connections.connect("default", host="localhost", port="19530")
    collection = Collection("paper_collection")
    collection.load()
    search_params = {
        "metric_type": "COSINE",
        "params": {"nprobe": 10}
    }

    ques = {"messages": [{"content": query, "role": "user"}]}
    res = get_embq_embedding(text=ques, appid=APPID, apikey=APIKEY, apisecret=APISecret)
    query_vector = parser_Message(res)
    results = collection.search(
        data=[query_vector],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["text"],
        filter=f"paper_id == {paper_id}"
    )

    retrieval = []
    if results:
        for result in results[0]:
            print(f"Text: {result.entity.get('text')}, Similarity score: {result.score}")
            retrieval.append(result.entity.get('text'))

    print(retrieval)
    return retrieval


def show_history(request):
    paper_id = request.GET.get('paper_id')
    histories = ChatHistory.objects.filter(eid=paper_id)
    init_messages(request, histories)
    messages = []
    for history in histories:
        if history.isUser:
            messages.append({'role': 'user', 'text': history.message})
        else:
            messages.append({'role': 'bot', 'text': history.message})
    response = {'msg': messages}
    return JsonResponse(response)


@csrf_exempt
def clear_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        paper_id = data.get('paper_id')
        if paper_id:
            ChatHistory.objects.filter(eid=paper_id).delete()
            request.session['history'] = []
            return JsonResponse({'status': 'success', 'message': '聊天记录已清空'})
        else:
            return JsonResponse({'status': 'error', 'message': '缺少 paper_id 参数'})
    return JsonResponse({'status': 'error', 'message': '请求方法不正确'})


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
        desc = {"messages": [{"content": document.page_content, "role": "user"}]}
        res = get_embp_embedding(desc, appid=APPID, apikey=APIKEY, apisecret=APISecret)
        vector = parser_Message(res)
        collection.insert([{"paper_id": paper_id, "embedding": vector, "text": document.page_content}])


# 向量数据库插入
def delete_collection(paper_id):
    collection = Collection("paper_collection")
    collection.load()
    collection.delete(expr=f"paper_id == {paper_id}")

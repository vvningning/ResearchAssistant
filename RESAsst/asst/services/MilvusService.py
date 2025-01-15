import time

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import connections, Collection

from asst.services.Embedding import get_embp_embedding, parser_Message

APPID = '9b60d12e'
APISecret = 'ZTUwYzNlZGNjMDhmNGQ5NDVjYThiZGEy'
APIKEY = 'c3bb38b3fc5fdc87ad9b1bc670c3e2e9'


# 向量数据库插入
def insert_collection(paper_id, content):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=40,
        length_function=len
    )
    split_docs = text_splitter.create_documents([content])
    connections.connect("default", host="localhost", port="19530")
    collection = Collection("paper_collection")
    collection.load()
    for i, document in enumerate(split_docs):
        time.sleep(0.3)
        desc = {"messages": [{"content": document.page_content, "role": "user"}]}
        res = get_embp_embedding(desc, appid=APPID, apikey=APIKEY, apisecret=APISecret)
        vector = parser_Message(res)
        collection.insert([{"id": str(paper_id)+"_"+str(i), "paper_id": paper_id, "embedding": vector, "text": document.page_content}])


# 向量数据库删除
def delete_collection(paper_id):
    connections.connect("default", host="localhost", port="19530")
    collection = Collection("paper_collection")
    collection.load()
    print("bingo", paper_id)
    id = str(paper_id)+"_%"
    collection.delete(expr=f"id like '{id}'")

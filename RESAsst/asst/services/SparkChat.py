from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

messages = []


def get_ans(prompt):
    messages.append(ChatMessage(
        role="user",
        content=prompt
    ))
    spark = ChatSparkLLM(
        spark_api_url="wss://spark-api.xf-yun.com/v3.1/chat",
        spark_app_id="9b60d12e",
        spark_api_key="c3bb38b3fc5fdc87ad9b1bc670c3e2e9",
        spark_api_secret="ZTUwYzNlZGNjMDhmNGQ5NDVjYThiZGEy",
        spark_llm_domain="generalv3",
        streaming=False,
    )
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    # print(a)
    messages.append(ChatMessage(
        role="assistant",
        content=a.generations[0][0].text
    ))
    return a.generations[0][0].text

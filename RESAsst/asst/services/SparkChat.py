from asst.services import SparkApi

MAX_TOKENS = 8000


def trim_history(messages):
    total_tokens = sum(len(msg["content"]) for msg in messages)
    while total_tokens > MAX_TOKENS:
        total_tokens -= len(messages[0]["content"])
        messages.pop(0)
    return messages


def get_ans(request, prompt):
    messages = request.session['history']
    print("message", messages)
    messages.append({"role": "user", "content": prompt})
    messages = trim_history(messages)
    SparkApi.answer = ""
    SparkApi.main(appid="9b60d12e",
                  api_key="c3bb38b3fc5fdc87ad9b1bc670c3e2e9",
                  api_secret="ZTUwYzNlZGNjMDhmNGQ5NDVjYThiZGEy",
                  Spark_url="wss://spark-api.xf-yun.com/v3.1/chat",
                  domain="generalv3",
                  question=messages)
    # print(SparkApi.answer)
    messages.append({"role": "assistant", "content": SparkApi.answer})
    messages = trim_history(messages)
    request.session['history'] = messages
    return SparkApi.answer


def init_messages(request, histories):
    messages = request.session.get('history', [])
    if not messages:
        for history in histories:
            if history.isUser:
                messages.append({"role": "user", "content": history.message})
            else:
                messages.append({"role": "assistant", "content": history.message})
    messages = trim_history(messages)
    request.session['history'] = messages

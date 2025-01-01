import requests
import hashlib
import random
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def translate(request):
    data = json.loads(request.body)
    text = data['text']
    print(text)

    app_id = '20241230002241792'
    secret_key = 'ly0fKph1cR04HNQJrCFP'
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = hashlib.md5((app_id + text + str(salt) + secret_key).encode()).hexdigest()
    params = {
        'q': text,
        'from': 'en',
        'to': 'zh',
        'appid': app_id,
        'salt': str(salt),
        'sign': sign
    }
    trans_response = requests.get(url, params=params)
    result = trans_response.json()

    return JsonResponse(result)
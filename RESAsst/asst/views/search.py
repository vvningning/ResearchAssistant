from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
import re

from asst.models import Build


def strmatch(request):
    keyword = request.GET.get('keyword')
    username = request.GET.get('user')
    results = Build.objects.filter(
        Q(name__icontains=keyword) | Q(content__icontains=keyword),
        username=username,
    )

    res = list()
    pattern = r".{0,150}" + re.escape(keyword) + r".{0,150}"
    for result in results:
        temp = re.findall(pattern, result.content, flags=re.DOTALL)
        if len(temp) > 0:
            result.content = temp[0]
            score = len(temp)
            res.append({'data': result, 'score': score})

    res = sorted(res, key=lambda x: x['score'], reverse=True)

    return JsonResponse(serializers.serialize("json", [item['data'] for item in res]), safe=False)


import json

from django.db.models import Q
from django.http import HttpResponse
from django.forms.models import model_to_dict
import re

from asst.models import Build

from es.driver import query


def strmatch(request):
    keyword = request.GET.get('keyword')
    username = request.GET.get('username')
    results = Build.objects.filter(
        Q(name__icontains=keyword) | Q(content__icontains=keyword),
        username=username,
    )

    res = list()
    pattern = r".{0,150}" + re.escape(keyword) + r".{0,150}"
    for result in results:
        temp = re.findall(pattern, result.content, flags=re.DOTALL)
        score = 0
        if len(temp) > 0:
            result.content = temp[0]
            score = score + len(temp)

        temp = re.findall(pattern, result.name, flags=re.DOTALL)
        if len(temp) > 0:
            if score == 0:
                score = 1
                result.content = result.content[:300]

        result.name = result.name.replace(keyword, '<font style="color:red;">' + keyword + '</font>')
        result.content = (result.content
                          .replace(keyword, '<font style="color:red;">' + keyword + '</font>')
                          .replace('\n', ' '))
        res.append({'data': result, 'score': score})

    res = sorted(res, key=lambda x: x['score'], reverse=True)
    res = [model_to_dict(item['data'], fields=['name', 'content']) for item in res]
    return HttpResponse(json.dumps(res, ensure_ascii=False))


def bm25(request):
    keyword = request.GET.get('keyword')
    username = request.GET.get('username')
    query_res = query(username, keyword)
    res = list()
    for item in query_res['hits']['hits']:
        highlight = item['highlight']
        source = item['_source']
        if 'name' in highlight:
            name = (highlight['name'][0]
                    .replace("<em>", '<font style="color:red;">')
                    .replace("</em>", '</font>'))
        else:
            name = source['name']

        if 'content' in highlight:
            content = (highlight['content'][0]
                       .replace("<em>", '<font style="color:red;">')
                       .replace("</em>", '</font>'))
        else:
            content = source['content'][:300]
        res.append({'name': name, 'content': content})

    return HttpResponse(json.dumps(res, ensure_ascii=False))

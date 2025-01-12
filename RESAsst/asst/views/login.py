import django
import pymysql
from django.db import connections
from django.http import HttpResponse, JsonResponse


def login(request):
    # 确保 Django 配置已初始化（如果在独立脚本中使用）
    django.setup()

    # 获取数据库连接
    conn = connections['default']

    username = request.GET.get('username')
    password = request.GET.get('password')
    res = False
    response = {}
    if username and password:
        cursor = conn.cursor()
        cursor.execute('SELECT username, password, email FROM asst_user WHERE username=%s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            print("OK")
            res = True
    response['username'] = username
    response['res'] = res
    print(response)
    return JsonResponse(response)

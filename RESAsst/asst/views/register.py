import django
from django.db import connections
from django.http import JsonResponse


def register(request):

    # 获取数据库连接
    conn = connections['default']

    username = request.GET.get('username')
    password = request.GET.get('password')
    email = request.GET.get('email')

    response = {'res': 0}

    cursor = conn.cursor()

    # 检查是否存在相同的 username
    cursor.execute("SELECT username FROM user WHERE username=%s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        response['res'] = 1 # 错误码，表示用户名已存在
        return JsonResponse(response)

    # 插入新记录
    cursor.execute("INSERT INTO user (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
    conn.commit()  # 提交更改

    cursor.close()
    conn.close()

    return JsonResponse(response)
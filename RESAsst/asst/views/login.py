import pymysql
from django.http import HttpResponse


def login(request):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='ftc020106',
        database='paper')

    username = request.GET.get('username')
    password = request.GET.get('password')
    res = False
    if username and password:
        cursor = conn.cursor()
        cursor.execute('SELECT username, password, email FROM user WHERE username=%s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            print("OK")
            res = True
    return HttpResponse(username, res)
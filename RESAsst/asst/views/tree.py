import json
import os
import shutil
from tkinter import filedialog

import PyPDF2
import mysql.connector
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from es.driver import add_index
from es.driver import delete_index

# 用来存储当前最大的eid（这里不考虑回收使用）
current_max_eid = 0
# 是从前端还是从后端获取
username = ""
# 相对路径"../pdf/test.pdf"要以/结尾
store_path = "../../../../前端/public/pdf"

# cursor = None

# 依据eid查询节点的path
def eid_to_path(eid):
    db = mysql.connector.connect(
        host="localhost",  # MySQL服务器地址
        user="test",  # 用户名
        password="123456",  # 密码
        database="asst"  # 数据库名称
    )
    cursor = db.cursor()
    # eid int类型，本节点的eid
    select_sql = "SELECT path FROM tree WHERE eid = %s"
    cursor.execute(select_sql, (eid,))
    result = cursor.fetchone()  # 获取一条记录
    if result:
        path = result[0]
        print(f"节点的 path: {path}")
    else:
        path = None
        print("未找到记录。")
    return path


# 转化path格式
def replace_eid_with_name(path):
    db = mysql.connector.connect(
        host="localhost",  # MySQL服务器地址
        user="test",  # 用户名
        password="123456",  # 密码
        database="asst"  # 数据库名称
    )
    cursor = db.cursor()
    # 拆分路径
    eids = path.strip('/').split('/')  # 去掉前后的 '/' 并按 '/' 分割
    names = []
    for eid in eids:
        select_sql = "SELECT name FROM tree WHERE eid = %s"
        cursor.execute(select_sql, (eid,))
        result = cursor.fetchone()  # 获取一条记录
        if result:
            name = result[0]  # 获取名称
            names.append(name)  # 将名称添加到列表
        else:
            names.append(f"未找到ID {eid}")  # 如果未找到对应的名称，可以添加占位符或处理逻辑
    # 将名称组合成新的路径
    new_path = '/' + '/'.join(names)
    return new_path


# 依据path查询节点的eid
def path_to_eid(path):
    db = mysql.connector.connect(
        host="localhost",  # MySQL服务器地址
        user="test",  # 用户名
        password="123456",  # 密码
        database="asst"  # 数据库名称
    )
    cursor = db.cursor()
    # path str类型，本节点的path
    select_sql = "SELECT eid FROM tree WHERE path = %s"
    cursor.execute(select_sql, (path,))
    result = cursor.fetchone()  # 获取一条记录
    if result:
        eid = result[0]
        print(f"节点的 eid: {eid}")
    else:
        eid = None
        print("未找到记录。")
    return eid


# 只用来拿到path，暂时不加和数据库比对
@csrf_exempt
def post_selected_node(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        path = data.get('node_path')
        print(path)
        if path:
            return JsonResponse({'status': 'success', 'message': 'get_the_path'})
        else:
            return JsonResponse({'status': 'error', 'message': 'lose_the_path'})
    return JsonResponse({'status': 'error', 'message': '请求方法不正确'})


def creat_folder_node(path, name, username):
    db = mysql.connector.connect(
        host="localhost",  # MySQL服务器地址
        user="test",  # 用户名
        password="123456",  # 密码
        database="asst"  # 数据库名称
    )
    cursor = db.cursor()
    # path str类型，父节点的path
    # name str类型，本节点的name
    global current_max_eid
    if path is None:
        new_path = f"/{current_max_eid + 1}"
    else:
        new_path = f"{path}/{current_max_eid + 1}"
    # print(new_path)
    cursor.execute('INSERT INTO tree VALUES (%s, %s, %s, %s, %s, %s)',
                   (current_max_eid + 1, name, "folder", new_path, None, username))
    db.commit()
    current_max_eid = current_max_eid + 1
    folder_path = store_path + replace_eid_with_name(new_path)
    print(folder_path)
    try:
        os.makedirs(folder_path, exist_ok=True)  # 如果文件夹已存在则不会报错
        print(f"已成功创建")
    except Exception as e:
        print(f"创建文件夹失败: {e}")
    return new_path


# 参数为父路径+节点名，需要返回一个本节点路径
@csrf_exempt
def post_new_folder(request):
    global username
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        message = data.get('message')
        parts = message.split('+')
        path = parts[0]
        name = parts[1]
        # 插入节点到数据库
        new_path = creat_folder_node(path, name, username)
        # print(path)
        if path:
            return JsonResponse({'status': 'success', 'message': new_path})
        else:
            return JsonResponse({'status': 'error', 'message': 'lose_the_message'})
    return JsonResponse({'status': 'error', 'message': '请求方法不正确'})


def creat_pdf_node(fpath, cpath, username):
    db = mysql.connector.connect(
        host="localhost",  # MySQL服务器地址
        user="test",  # 用户名
        password="123456",  # 密码
        database="asst"  # 数据库名称
    )
    cursor = db.cursor()
    # fpath str类型，父节点的path
    # cpath str类型，本节点的path，文件本地路径
    global current_max_eid

    pdf_file = open(cpath, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    text = ""
    # 循环遍历每一页并提取文本
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    pdf_file.close()
    filename = os.path.basename(cpath)
    # print(filename)
    # filename = cpath.rsplit('\\', 1)[-1]
    new_path = f"{fpath}/{current_max_eid + 1}"  # 构建新的 path
    # print(new_path)
    cursor.execute('INSERT INTO tree VALUES (%s, %s, %s, %s, %s, %s)',
                   (current_max_eid + 1, filename, "pdf", new_path, text, username))
    db.commit()
    current_max_eid = current_max_eid + 1
    add_index(current_max_eid, username, filename, text)
    document_path = store_path + replace_eid_with_name(new_path)
    print(document_path)
    try:
        # 复制文件到目标路径
        shutil.copy(cpath, document_path)
        print(f"文件已上传")
    except Exception as e:
        print(f"上传文件时发生错误: {e}")
    return new_path


# 参数为父路径，需要返回一个本节点路径+节点名
@csrf_exempt
def post_new_document(request):
    global username
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        path = data.get('active_document_path')
        # print(path)
        pdf_file_path = filedialog.askopenfilename(title="选择PDF文件", filetypes=[("PDF files", "*.pdf")])
        if pdf_file_path:
            new_path = creat_pdf_node(path, pdf_file_path, username)
        # 获取文件名,保留4位
        file_name = os.path.basename(pdf_file_path)
        first_four_chars = file_name[:4]
        message = new_path + '+' + first_four_chars
        if path:
            return JsonResponse({'status': 'success', 'message': message})
        else:
            return JsonResponse({'status': 'error', 'message': 'lose_the_path'})
    return JsonResponse({'status': 'error', 'message': '请求方法不正确'})


# 删除此节点以及其所有子节点，返回父节点路径
def delete_node(path):
    db = mysql.connector.connect(
        host="localhost",  # MySQL服务器地址
        user="test",  # 用户名
        password="123456",  # 密码
        database="asst"  # 数据库名称
    )
    cursor = db.cursor()
    # path str类型，本节点的path
    query = """
    SELECT
        e2.eid
    FROM
        tree e1,
        tree e2 
    WHERE
        e1.path = %s 
        AND e2.path LIKE concat( e1.path, '/%' );
    """
    cursor.execute(query, (path,))
    results = cursor.fetchall()
    # print(results)
    if results:
        eids_to_delete = [eid[0] for eid in results]  # 提取 eid
        ceid = path_to_eid(path)  # 当前节点 eid
        delete_index(ceid)
        eids_to_delete.append(ceid)
        print(f"将要删除的节点的 ID: {eids_to_delete}")
        delete_query = "DELETE FROM tree WHERE eid IN (%s)" % ','.join(['%s'] * len(eids_to_delete))
        cursor.execute(delete_query, eids_to_delete)
        # 提交更改
        db.commit()
        print(f"已成功删除 {cursor.rowcount} 条记录")
    else:
        cursor.execute("SELECT * FROM tree WHERE path = %s", (path,))
        nodes = cursor.fetchall()
        if not nodes:
            print(f"No nodes found with path: {path}")
            return
        # 删除节点
        cursor.execute("DELETE FROM tree WHERE path = %s", (path,))
        db.commit()
        print("已成功删除1条记录")


def delete_path(node_path):
    if os.path.isfile(node_path):
        try:
            os.remove(node_path)
            print(f"Deleted file: {node_path}")
        except Exception as e:
            print(f"Error deleting file {node_path}: {e}")
    elif os.path.isdir(node_path):
        try:
            shutil.rmtree(node_path)
            print(f"Deleted directory: {node_path}")
        except Exception as e:
            print(f"Error deleting directory {node_path}: {e}")
    else:
        print(f"Path does not exist: {node_path}")


# 参数为节点路径，加入删除当前节点和所有子节点的逻辑
@csrf_exempt
def post_deleted_node(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        path = data.get('node_path')
        node_path = store_path + replace_eid_with_name(path)
        delete_node(path)
        print(node_path)
        delete_path(node_path)
        # print(path)
        if path:
            return JsonResponse({'status': 'success', 'message': 'get_the_path'})
        else:
            return JsonResponse({'status': 'error', 'message': 'lose_the_path'})
    return JsonResponse({'status': 'error', 'message': '请求方法不正确'})


def get_nodes_list(request):
    global username
    # print(request.GET.get('username'))
    # data = [
    #     {"name": "node1", "type": "folder", "path": "/1"},
    #     {"name": "node2", "type": "document", "path": "/1/2"},
    #     {"name": "node3", "type": "folder", "path": "/1/3"},
    #     {"name": "node4", "type": "folder", "path": "/1/2/4"},
    # ]
    db = mysql.connector.connect(
        host="localhost",  # MySQL服务器地址
        user="test",  # 用户名
        password="123456",  # 密码
        database="asst"  # 数据库名称
    )
    cursor = db.cursor()
    username = request.GET.get('username')
    query = "SELECT name, type, path FROM tree WHERE username = %s"
    cursor.execute(query, (username,))
    results = cursor.fetchall()
    data = []
    if not results:  # 说明是一个新用户
        path = creat_folder_node(None, "root_node", username)
        data.append({"name": "root", "type": "folder", "path": path})
    else:
        for name, type_, path in results:
            node_name = name[:4]
            if type_ == "pdf":
                type_ = "document"  # 转换类型为 'document'
            data.append({"name": node_name, "type": type_, "path": path})
    return JsonResponse(data, safe=False)

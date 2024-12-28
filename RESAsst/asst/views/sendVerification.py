import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.http import JsonResponse



import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re


# 生成随机验证码
def generate_verification_code(length=6):
    return ''.join(random.choices(string.digits, k=length))


# 配置邮件发送参数
def send_email(receiver_email, verification_code):
    # 1.准备工作：登录邮箱
    # smtp服务器地址
    mail_host = "smtp.163.com"
    # 发送方的邮箱账号
    mail_sender = "18913805248@163.com"
    # 发送方的授权码，注意不是邮箱的登录密码，而是开启smtp协议时的授权码
    mail_pwd = "ZUgVfQ3PJdKq6veN"
    # 连接邮箱对象
    smtp = smtplib.SMTP_SSL(mail_host, 465)
    # 登录邮箱
    smtp.login(mail_sender, mail_pwd)

    # 2.准备数据：构建邮件内容
    # 正文内容
    data = MIMEMultipart()
    # 邮件内容
    body = f'您的验证码是: {verification_code}'
    data.attach(MIMEText(body, 'plain'))
    # 邮件主题/标题
    data["Subject"] = "验证码"
    # 发送方
    data["From"] = mail_sender
    # 接收方
    receivers = [receiver_email]
    data["To"] = ";".join(receivers)

    # 3.发送邮件
    # 发送
    try:
        smtp.sendmail(mail_sender, receivers, data.as_string())
    except Exception as e:
        print(f"发送邮件时发生错误: {e}")
    # 退出
    smtp.quit()


# 测试发送邮件
def sendVerification(request):
    response = {}
    # 生成验证码
    verification_code = generate_verification_code()

    # 发送验证码邮件
    receiver_email = request.GET.get('email')  # 收件人邮箱地址
    send_email(receiver_email, verification_code)

    response["verification_code"] = verification_code
    return JsonResponse(response)

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    email = models.CharField(max_length=255, verbose_name='邮箱')


class Build(models.Model):
    eid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='文件名')
    type = models.CharField(max_length=100, verbose_name='文件类型')
    path = models.CharField(max_length=200, verbose_name='文件路径')
    content = models.TextField(verbose_name='文件内容')
    username = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)

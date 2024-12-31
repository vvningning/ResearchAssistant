from django.db import models
from django.db.models import Max


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


class ChatHistory(models.Model):
    msgId = models.IntegerField(verbose_name='消息序号')
    eid = models.ForeignKey(Build, to_field='eid', on_delete=models.CASCADE)
    isUser = models.BooleanField(verbose_name='消息对象')
    message = models.TextField(verbose_name='消息内容')

    class Meta:
        unique_together = ('id', 'eid')

    def save(self, *args, **kwargs):
        if not self.msgId:
            max_id = ChatHistory.objects.filter(eid=self.eid).aggregate(Max('id'))['id__max']
            if max_id is None:
                self.msgId = 1
            else:
                self.msgId = max_id + 1
        super().save(*args, **kwargs)

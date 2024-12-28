from django.db import models

# Create your models here.
class Build(models.Model):
    eid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    content = models.TextField()
    username = models.CharField(max_length=20)

from django.db import models

# Create your models here.
class Useragent(models.Model):
    useragent = models.TextField(unique=True)
    count = models.IntegerField()

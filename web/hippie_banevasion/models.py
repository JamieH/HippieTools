from django.db import models

# Create your models here.
class Useragent(models.Model):
    useragent_hash = models.CharField(unique=True, max_length=64)
    useragent = models.TextField()
    count = models.IntegerField()

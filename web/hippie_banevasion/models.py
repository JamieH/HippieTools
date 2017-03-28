from django.db import models

# Create your models here.


class Useragent(models.Model):
    useragent_hash = models.CharField(unique=True, max_length=64)
    useragent = models.TextField()
    count = models.IntegerField()


class ByondVersion(models.Model):
    byondversion = models.IntegerField(unique=True)
    count = models.IntegerField()


class ClientBlob(models.Model):
    fingerprint = models.CharField(max_length=32, unique=True)


class Client(models.Model):
    ckey = models.CharField(max_length=255, unique=True)
    fingerprints = models.ManyToManyField(ClientBlob)
    related_accounts = models.ManyToManyField("self")
    first_seen = models.DateTimeField(auto_now_add=True, blank=True)
    last_seen = models.DateTimeField(blank=True)
    byondversions = models.ManyToManyField(ByondVersion)
    useragents = models.ManyToManyField(Useragent)




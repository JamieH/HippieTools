from django.db import models
from .enums import SecurityEventEnum
from django_enumfield import EnumField

# Create your models here.


class Useragent(models.Model):
    useragent_hash = models.CharField(unique=True, max_length=64)
    useragent = models.TextField()
    count = models.IntegerField()

    def __str__(self):
        return self.useragent

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')


class IPAddress(models.Model):
    ip = models.GenericIPAddressField()

    def __str__(self):
        return str(self.ip)

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')


class ByondVersion(models.Model):
    byondversion = models.IntegerField(unique=True)
    count = models.IntegerField()

    def __str__(self):
        return "{}".format(self.byondversion)

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')


class ClientBlob(models.Model):
    fingerprint = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.fingerprint

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')


class Client(models.Model):
    ckey = models.CharField(max_length=255, unique=True)
    fingerprints = models.ManyToManyField(ClientBlob)
    related_accounts = models.ManyToManyField("self")
    first_seen = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_seen = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_post = models.DateTimeField(blank=True, null=True)
    byond_versions = models.ManyToManyField(ByondVersion)
    useragents = models.ManyToManyField(Useragent)
    reverse_engineer = models.BooleanField(default=False)
    ips = models.ManyToManyField(IPAddress)

    def __str__(self):
        return self.ckey

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')

class SecurityEvent(models.Model):
    client = models.ForeignKey(Client, null=True, blank=True)
    ip = models.ForeignKey(IPAddress, null=True, blank=True)
    useragent = models.ForeignKey(Useragent, null=True, blank=True)
    event_type = EnumField(SecurityEventEnum)
    data = models.TextField()

    class Meta:
        default_permissions = ('add', 'change', 'delete', 'view')

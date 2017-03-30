from django.contrib import admin
from hippie_banevasion import models
# Register your models here.

admin.site.register(models.Client)
admin.site.register(models.ClientBlob)
admin.site.register(models.Useragent)
admin.site.register(models.ByondVersion)

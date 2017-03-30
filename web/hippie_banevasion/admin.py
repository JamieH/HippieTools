from django.contrib import admin
from hippie_banevasion import models
# Register your models here.


class ByondVersionInline(admin.StackedInline):
    model = models.Client.byond_versions.through


class UseragentInline(admin.StackedInline):
    model = models.Client.useragents.through


class ClientBlobInline(admin.StackedInline):
    model = models.Client.fingerprints.through


class ClientAdmin(admin.ModelAdmin):
    list_display = ("ckey", "first_seen", "last_seen", "last_post", "reverse_engineer")
    inlines = [ByondVersionInline, UseragentInline, ClientBlobInline]


class ClientBlobAdmin(admin.ModelAdmin):
    inlines = [ClientBlobInline]


class UseragentAdmin(admin.ModelAdmin):
    inlines = [UseragentInline]


class ByondVersionAdmin(admin.ModelAdmin):
    inlines = [ByondVersionInline]


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.ClientBlob, ClientBlobAdmin)
admin.site.register(models.Useragent, UseragentAdmin)
admin.site.register(models.ByondVersion, ByondVersionAdmin)

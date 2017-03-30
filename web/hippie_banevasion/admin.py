from django.contrib import admin
from hippie_banevasion import models
# Register your models here.


class ByondVersionInline(admin.StackedInline):
    model = models.ByondVersion


class UseragentInline(admin.StackedInline):
    model = models.Useragent


class ClientBlobInline(admin.StackedInline):
    model = models.ClientBlob


class ClientInline(admin.StackedInline):
    model = models.Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ("ckey", "first_seen", "last_seen", "last_post", "reverse_engineer")
    inlines = ("ByondVersionInline", "UseragentInline", "ClientBlobInline",)


class ClientBlobAdmin(admin.ModelAdmin):
    inlines = ("ClientInline",)


class UseragentAdmin(admin.ModelAdmin):
    inlines = ("ClientInline",)


class ByondVersionAdmin(admin.ModelAdmin):
    inlines = ("ClientInline",)


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.ClientBlob, ClientBlobAdmin)
admin.site.register(models.Useragent, UseragentAdmin)
admin.site.register(models.ByondVersion, ByondVersionAdmin)

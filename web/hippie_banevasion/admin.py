from django.contrib import admin
from django.urls import reverse
from django.utils.html import mark_safe

from hippie_banevasion import models
# Register your models here.


class ByondVersionInline(admin.TabularInline):
    model = models.Client.byond_versions.through
    extra = 0
    readonly_fields = ['link']

    def link(self, obj):
        url = reverse(...)
        return mark_safe("<a href='%s'>view</a>" % url)

    # the following is necessary if 'link' method is also used in list_display
    link.allow_tags = True


class UseragentInline(admin.TabularInline):
    model = models.Client.useragents.through
    extra = 0
    readonly_fields = ['link']

    def link(self, obj):
        url = reverse(...)
        return mark_safe("<a href='%s'>view</a>" % url)

    # the following is necessary if 'link' method is also used in list_display
    link.allow_tags = True


class ClientBlobInline(admin.TabularInline):
    model = models.Client.fingerprints.through
    extra = 0
    readonly_fields = ['link']

    def link(self, obj):
        url = reverse(...)
        return mark_safe("<a href='%s'>view</a>" % url)

    # the following is necessary if 'link' method is also used in list_display
    link.allow_tags = True


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

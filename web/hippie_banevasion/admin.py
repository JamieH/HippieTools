from django.contrib import admin
from hippie_banevasion import models
# Register your models here.


class ByondVersionInline(admin.StackedInline):
    model = models.Client.byond_versions.through
    extra = 0


class UseragentInline(admin.StackedInline):
    model = models.Client.useragents.through
    extra = 0


class ClientBlobInline(admin.StackedInline):
    model = models.Client.fingerprints.through
    extra = 0


class ClientRelatedAccountsInline(admin.StackedInline):
    model = models.Client.related_accounts.though
    extra = 0


class ClientAdmin(admin.ModelAdmin):
    list_display = ("ckey", "first_seen", "last_seen", "last_post", "reverse_engineer")
    search_fields = ('ckey',)
    inlines = [ClientRelatedAccountsInline, ByondVersionInline, UseragentInline, ClientBlobInline]
    exclude = ('byond_versions','useragents','fingerprints','related_accounts',)


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

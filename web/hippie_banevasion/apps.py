from django.apps import AppConfig


class HippieBanEvasionConfig(AppConfig):
    name = 'hippie_banevasion'

    def ready(self):
        from django_evercookie.config import settings
        # Changing cookie names for Etag storage
        settings.etag_cookie_name = 'etagstorage'
        # Enabling CSS History Knocking
        settings.history = 'true'
        # Setting Django's STATIC_URL manually
        settings.static_url = '/static/'
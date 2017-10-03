from xenforo_auth.provider import XenforoProvider
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns


urlpatterns = default_urlpatterns(XenforoProvider)
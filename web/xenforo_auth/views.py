import requests

from allauth.socialaccount import app_settings
from xenforo_auth.provider import XenforoProvider
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from xenforo_auth.client import  XenforoOAuth2Client

class XenforoOAuth2Adapter(OAuth2Adapter):
    provider_id = XenforoProvider.id
    settings = app_settings.PROVIDERS.get(provider_id, {})
    web_url = 'https://hippiestation.com'

    # https://hippiestation.com/api/index.php?oauth/authorize&response_type=code&client_id=9lbfag0p9q&scope=read&redirect_uri=http%3A%2F%2Ftools.hippiestation.com%2FbdApi%2Fphp_demo%2Findex.php%3Faction%3Dcallback
    # https://hippiestation.com/api/index.php?oauth/authorize?client_id=9lbfag0p9q&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Faccounts%2Fxenforo%2Flogin%2Fcallback%2F&scope=&response_type=code&state=meb9vY0Buo7i
    authorize_url = '{0}/api/index.php'.format(web_url)
    access_token_url = '{0}/api/index.php'.format(web_url)
    profile_url = '{0}/api/index.php?users/me'.format(web_url)

    def complete_login(self, request, app, token, **kwargs):
        print(token)
        params = {'oauth_token': token.token}
        resp = requests.get(self.profile_url, params=params)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(
            request, extra_data
        )


class XenforoAuth2CallbackView(OAuth2CallbackView):
    def get_client(self, request, app):
        client = super(XenforoAuth2CallbackView, self).get_client(request,
                                                                   app)
        xenforo_client = XenforoOAuth2Client(
            client.request, client.consumer_key, client.consumer_secret,
            client.access_token_method, client.access_token_url,
            client.callback_url, client.scope)
        return xenforo_client


class XenforoOAuth2LoginView(OAuth2LoginView):
    def get_client(self, request, app):
        client = super(XenforoOAuth2LoginView, self).get_client(request,
                                                                   app)
        xenforo_client = XenforoOAuth2Client(
            client.request, client.consumer_key, client.consumer_secret,
            client.access_token_method, client.access_token_url,
            client.callback_url, client.scope)
        return xenforo_client

oauth2_login = XenforoOAuth2LoginView.adapter_view(XenforoOAuth2Adapter)
oauth2_callback = XenforoAuth2CallbackView.adapter_view(XenforoOAuth2Adapter)

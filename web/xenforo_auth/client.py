import requests
import re

from allauth.socialaccount.providers.oauth2.client import (
    OAuth2Client,
    OAuth2Error,
)


class XenforoOAuth2Client(OAuth2Client):
    def get_redirect_url(self, authorization_url, extra_params):
        url = super(XenforoOAuth2Client, self).get_redirect_url(authorization_url, extra_params)
        print(url)
        url = url.replace("index.php?", "index.php?oauth/authorize&")
        url = re.sub(r'&scope=.\+.\+.\+.', '&scope=read', url)
        print(url)
        return url

    def get_access_token(self, code):
        payload = {
            'grant_type': 'authorization_code',
            'client_id': self.consumer_key,
            'client_secret': self.consumer_secret,
            'code': code,
            'redirect_uri': self.callback_url,
        }
        self._strip_empty_keys(payload)

        url = self.access_token_url
        url = url.replace("index.php", "index.php?oauth/token")
        resp = requests.post(url, data=payload)
        access_token = None
        if resp.status_code == 200:
            access_token = resp.json()
        if not access_token or 'access_token' not in access_token:
            raise OAuth2Error('Error retrieving access token: %s'
                              % resp.content)
        return access_token

from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class XenforoAccount(ProviderAccount):
    def get_profile_url(self):
        return None

    def get_avatar_url(self):
        return None


class XenforoProvider(OAuth2Provider):
    id = 'xenforo'
    name = 'Xenforo'
    account_class = XenforoAccount
    access_token_method = "POST"

    def get_default_scope(self):
        return ["read",]

    def extract_uid(self, data):
        return str(data['user']['user_id'])

    def extract_common_fields(self, data):
        user = data.get('user')
        fields = user.get('user_fields')
        ckey = fields.get('ckey')
        ckey_value = ckey.get('value')

        return dict(email=user.get('user_email'),
                    username=ckey_value,
                    name=data.get('username'))

provider_classes = [XenforoProvider]
from hippie_banevasion.utils import utils
from hippie_banevasion.enums import SecurityEventEnum

from django.conf import settings
from django.http import Http404

# Request must come from the game server IP
class ComesFromGameserver(object):
    def dispatch(self, request, *args, **kwargs):
        client_ip = utils.get_client_ip(request)
        if client_ip != settings.GAME_SERVER_IP:
            msg = "Request from invalid IP: {} does not match configured gameserver IP: {}".format(client_ip, settings.GAME_SERVER_IP)
            utils.store_security_event(
                request,
                'gameip_missmatch',
                data=msg
            )
            print(msg)
            raise Http404()

        return super(ComesFromGameserver, self).dispatch(
            request, *args, **kwargs)

# Request must have a body
class HasBody(object):
    def dispatch(self, request, *args, **kwargs):
        data = request.GET.get('body', '')
        if request.method == "GET" and data == '':
            msg = "Request did not specify a body, possible RE attemptRe"
            utils.store_security_event(
                request,
                'no_body',
                data=msg
            )
            raise Http404()
        return super(HasBody, self).dispatch(
            request, *args, **kwargs)

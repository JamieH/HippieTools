from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import resolve
from hippie_admin.utils import fmt
from hippie_ss13.models import Player

def check_rank(get_response):
    def middleware(request):
        path = request.META['PATH_INFO']
        if "hippie_admin" not in resolve(path).app_names:
            response = get_response(request)
            return response

        path = path.rstrip("/")
        if path not in ["/accounts/login", "/accounts/xenforo/login", "/accounts/xenforo/login/callback"]:
            if not request.user.is_authenticated():
                return HttpResponseRedirect("/accounts/login")
        else:
            response = get_response(request)
            return response

        ckey = fmt.ckey(request.user.username)
        request.current_player = Player.objects.get(ckey=ckey)

        if request.current_player.get_rank() not in ["Host", "HeadAdmin", "GameMaster", "GameAdmin"]:
            logout(request)
            return HttpResponseForbidden("You should not be here!")

        response = get_response(request)
        return response

    return middleware

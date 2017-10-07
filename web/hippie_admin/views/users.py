import operator
import functools

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic.list import ListView

from hippie_banevasion.models import Client
from hippie_ss13.models import Player
from hippie_admin.utils import fmt


@login_required
def user_show(request, ckey, template_name='hippie_admin/users/show.html'):
    player = get_object_or_404(Player, ckey=fmt.ckey(ckey))
    client = None
    alts = None

    try:
        client = Client.objects.get(ckey=player.ckey)
    except Client.DoesNotExist:
        pass
    else:
        hbest_alts = client.get_alts()
        ip_alts = player.get_ip_alts()
        cid_alts = player.get_cid_alts()
        ip_cid_alts = set(ip_alts) - (set(ip_alts) - set(cid_alts))


    context = {
        'player': player,
        'client': client,
        'hbest_alts': hbest_alts,
        'ip_alts': ip_alts,
        'cid_alts': cid_alts,
        'ip_cid_alts': ip_cid_alts,
        'total_alts': len(ip_alts) + len(cid_alts) + len(hbest_alts)
    }
    return render(request, template_name, context)


class UserListView(LoginRequiredMixin, ListView):
    """
    Display a Blog List page filtered by the search query.
    """
    model = Player
    paginate_by = 30
    template_name = "hippie_admin/users/list.html"

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data()
        context['q'] = self.request.GET.get('q') or ""
        return context

    def get_queryset(self):
        result = super(UserListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                functools.reduce(operator.and_,
                                 (Q(ckey__icontains=q) for q in query_list))
            )

        return result

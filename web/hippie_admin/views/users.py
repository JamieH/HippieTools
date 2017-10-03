import operator
import functools

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic.list import ListView

from hippie_banevasion.models import Client


@login_required
def user_show(request, pk, template_name='hippie_admin/users/show.html'):
    client = get_object_or_404(Client, pk=pk)
    return render(request, template_name, {'client':client})

class UserListView(LoginRequiredMixin, ListView):
    """
    Display a Blog List page filtered by the search query.
    """
    model = Client
    paginate_by = 30
    template_name = "hippie_admin/users/list.html"

    def get_queryset(self):
        result = super(ListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                functools.reduce(operator.and_,
                       (Q(ckey__icontains=q) for q in query_list)) |
                functools.reduce(operator.and_,
                       (Q(ips__ip__icontains=q) for q in query_list))
            )

        return result
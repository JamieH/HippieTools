import operator
import functools

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic.list import ListView

from hippie_banevasion.models import Client


class ConnectionListView(LoginRequiredMixin, ListView):
    """
    Display a Blog List page filtered by the search query.
    """
    model = Client
    paginate_by = 30
    template_name = "hippie_admin/connections/list.html"

    def get_queryset(self):
        result = super(ListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                functools.reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                functools.reduce(operator.and_,
                       (Q(content__icontains=q) for q in query_list))
            )

        return result

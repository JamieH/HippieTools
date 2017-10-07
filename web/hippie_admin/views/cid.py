from django.views.generic import TemplateView
from hippie_ss13.models import ConnectionLog, Player


class CIDView(TemplateView):
    template_name = "hippie_admin/cid/show.html"

    def dispatch(self, request, *args, **kwargs):
        self.cid =  kwargs.get('cid')
        return super(CIDView, self).dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super(CIDView, self).get_context_data(**kwargs)
        ckeys = ConnectionLog.objects.filter(computerid=self.cid).values_list('ckey', flat=True).distinct()
        context['cid'] = self.cid
        context['players'] = Player.objects.filter(ckey__in=ckeys)
        return context

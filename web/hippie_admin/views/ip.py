from django.views.generic import TemplateView
from hippie_ss13.models import ConnectionLog, Player
import hippie_admin.utils.format as fmt


class IPView(TemplateView):
    template_name = "hippie_admin/ip/show.html"

    def dispatch(self, request, *args, **kwargs):
        self.rawip =  kwargs.get('ip')
        self.ip =  fmt.ip_int(self.rawip)
        return super(IPView, self).dispatch(request, args, kwargs)

    def get_context_data(self, **kwargs):
        context = super(IPView, self).get_context_data(**kwargs)
        ckeys = ConnectionLog.objects.filter(ip=self.ip).values_list('ckey', flat=True).distinct()
        context['ip'] = self.rawip
        context['players'] = Player.objects.filter(ckey__in=ckeys)
        return context

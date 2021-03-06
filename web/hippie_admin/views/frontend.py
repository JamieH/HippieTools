from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic import TemplateView
from hippie_ss13.models import Messages, MentorMemo


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "hippie_admin/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['memos'] = Messages.objects.filter(type='memo').order_by('-timestamp')
        context['mentor_memos'] = MentorMemo.objects.order_by('-timestamp')
        return context

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic import TemplateView
from hippie_ss13.models import Memo, MentorMemo

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "hippie_admin/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['memos'] = Memo.objects.all().order_by('-timestamp')
        context['mentor_memos'] = MentorMemo.objects.all().order_by('-timestamp')
        return context

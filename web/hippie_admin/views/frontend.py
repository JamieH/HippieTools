from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic import TemplateView

class home(LoginRequiredMixin, TemplateView):
    template_name = "hippie_admin/home.html"
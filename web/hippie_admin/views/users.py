from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from hippie_banevasion.models import Client

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['ckey',]

def user_list(request, template_name='hippie_admin/users/list.html'):
    client = Client.objects.all()
    data = {}
    data['object_list'] = client
    return render(request, template_name, data)

def user_show(request, pk, template_name='hippie_admin/users/user.html'):
    client= get_object_or_404(Client, pk=pk)
    form = ClientForm(id=pk)
    return render(request, template_name, {'form':form})

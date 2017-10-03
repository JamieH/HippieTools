from django.shortcuts import render, redirect, get_object_or_404

from hippie_banevasion.models import Client

def user_list(request, template_name='hippie_admin/users/list.html'):
    client = Client.objects.all()
    data = {}
    data['object_list'] = client
    return render(request, template_name, data)

def user_show(request, pk, template_name='hippie_admin/users/user.html'):
    client = get_object_or_404(Client, pk=pk)
    return render(request, template_name, {'client':client})

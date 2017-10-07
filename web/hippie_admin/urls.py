"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from hippie_admin.views import frontend, users, bans, connections, notes, admins, cid, ip

from django.conf import settings
from django.conf.urls.static import static

app_name="hippie_admin"
urlpatterns = [
    url(r'^$', frontend.HomeView.as_view(), name='home'),

    url(r'^admins/$', admins.AdminListView.as_view(), name='admin_list'),

    url(r'^bans/$', bans.BanListView.as_view(), name='ban_list'),

    url(r'^notes/$', notes.NoteListView.as_view(), name='note_list'),

    url(r'^connections/$', connections.ConnectionListView.as_view(), name='connection_list'),

    url(r'^users/$', users.UserListView.as_view(), name='user_list'),
    url(r'^users/(?P<ckey>[a-z0-9]+)$', users.user_show, name='user_show'),

    url(r'^cid/(?P<cid>[a-z0-9]+)$', cid.CIDView.as_view(), name='cid_show'),
    url(r'^ip/(?P<ip>[0-9.]+)$', ip.IPView.as_view(), name='ip_show'),

    url(r'^accounts/', include('allauth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

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
from django.contrib import admin

from hippie_admin.views import frontend, users

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', frontend.home.as_view(), name='home'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^users/$', users.user_list, name='user_list'),
    url(r'^users/(?P<pk>\d+)$', users.user_show, name='user_show'),
    url(r'^accounts/', include('allauth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

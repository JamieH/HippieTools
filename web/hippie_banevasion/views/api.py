from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse, Http404

from hippie_banevasion import models

import json
import time
import hmac
import hashlib

def get_useragent(request):
    return request.META['HTTP_USER_AGENT']

def store_useragent(request):
    useragent = get_useragent(request)

    hash_object = hashlib.sha256(bytes(useragent, 'ascii'))
    useragent_hash = hash_object.hexdigest()

    try:
        useragent_obj = models.Useragent.objects.get(useragent_hash=useragent_hash)
        useragent_obj.count += 1
        useragent_obj.save(update_fields=["count"])
    except models.Useragent.DoesNotExist:
        useragent_obj = models.Useragent.objects.create(useragent_hash=useragent_hash, useragent=useragent, count=1)
        useragent_obj.save()

class get_protected_data_view(View):
    def get(self, request, *args, **kwargs):
        data = request.GET.get('body', '')
        if data == '':
            raise Http404()

        data_obj = json.loads(data)
        data_obj['time'] = time.time()
        data = json.dumps(data_obj)

        dig = hmac.new(bytearray(settings.TANGO_HMAC_KEY, 'ascii'), msg=bytearray(data, 'ascii'), digestmod=hashlib.sha256).hexdigest()

        response = HttpResponse(dig, content_type='text/plain')
        response['Content-Length'] = len(dig)
        return response

class client_view(View):
    def get(self, request, *args, **kwargs):
        store_useragent(request)
        return HttpResponse('')

    def post(self, request, *args, **kwargs):
        return HttpResponse('')
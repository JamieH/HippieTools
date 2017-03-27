from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse, Http404

from hippie_banevasion import models
from hippie_banevasion.crypto import AESCipher

import json
import time
import hmac
import hashlib

def get_useragent(request):
    return request.META['HTTP_USER_AGENT']

def store_useragent(useragent):
    hash_object = hashlib.sha256(bytes(useragent, 'ascii'))
    useragent_hash = hash_object.hexdigest()

    try:
        useragent_obj = models.Useragent.objects.get(useragent_hash=useragent_hash)
        useragent_obj.count += 1
        useragent_obj.save(update_fields=["count"])
    except models.Useragent.DoesNotExist:
        useragent_obj = models.Useragent.objects.create(useragent_hash=useragent_hash, useragent=useragent, count=1)
        useragent_obj.save()

def store_byondversion(byondversion):
    try:
        byondversion_obj = models.ByondVersion.objects.get(byondversion=byondversion)
        byondversion_obj.count += 1
        byondversion_obj.save(update_fields=["count"])
    except models.ByondVersion.DoesNotExist:
        byondversion_obj = models.ByondVersion.objects.create(byondversion=byondversion, count=1)
        byondversion_obj.save()

class get_protected_data_view(View):
    def get(self, request, *args, **kwargs):
        data = request.GET.get('body', '')
        if data == '':
            raise Http404()

        data_obj = json.loads(data)
        data_obj['time'] = time.time()
        data = json.dumps(data_obj)

        encryption = AESCipher("SskXwgkBx77C5Ya8")
        data = encryption.encrypt(data)

        dig = hmac.new(bytearray(settings.TANGO_HMAC_KEY, 'ascii'), msg=bytearray(data, 'ascii'), digestmod=hashlib.sha256).hexdigest()

        body = "{}{}".format(dig, data)

        response = HttpResponse(body, content_type='text/plain')
        response['Content-Length'] = len(body)
        return response

class client_view(View):
    def get(self, request, *args, **kwargs):
        useragent = get_useragent(request)

        data = request.GET.get('body', '')
        if data == '':
            print("Request did not specify a body, possible RE attempt")
            raise Http404()

        sent_hmac = data[:64]
        body = data[64:len(data)]

        correct_hmac = hmac.new(bytearray(settings.TANGO_HMAC_KEY, 'ascii'), msg=bytearray(body, 'ascii'), digestmod=hashlib.sha256).hexdigest()

        if correct_hmac != sent_hmac:
            print("Error verifiying HMAC... {} != {}".format(sent_hmac, correct_hmac))
            raise Http404()

        encryption = AESCipher("SskXwgkBx77C5Ya8")
        data = encryption.decrypt(body)

        store_useragent(useragent)

        data_obj = json.loads(data)
        print(data_obj)

        store_byondversion(data_obj['byond_version'])
        return HttpResponse('')

    def post(self, request, *args, **kwargs):
        return HttpResponse('')
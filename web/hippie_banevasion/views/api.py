from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from django.conf import settings
from django.http import HttpResponse, Http404
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator

from hippie_banevasion import models
from hippie_banevasion.crypto import AESCipher

import json
import time
import hmac
import hashlib

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

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

def decode_encrypted_data(data):
    sent_hmac = data[:64]
    body = data[64:len(data)]

    correct_hmac = hmac.new(bytearray(settings.TANGO_HMAC_KEY, 'ascii'), msg=bytearray(body, 'ascii'),
                            digestmod=hashlib.sha256).hexdigest()

    if correct_hmac != sent_hmac:
        print("Error verifiying HMAC... {} != {}".format(sent_hmac, correct_hmac))
        raise Http404()

    encryption = AESCipher("SskXwgkBx77C5Ya8")
    decrypted_data = encryption.decrypt(body)

    data_obj = json.loads(decrypted_data)
    print(data_obj)
    return data_obj

@method_decorator(xframe_options_exempt, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class client_view(View):
    def get(self, request, *args, **kwargs):
        useragent = get_useragent(request)

        data = request.GET.get('body', '')
        if data == '':
            print("Request did not specify a body, possible RE attempt")
            raise Http404()

        data_obj = decode_encrypted_data(data)

        store_useragent(useragent)
        store_byondversion(data_obj['byond_version'])

        print(get_client_ip(request))

        if get_client_ip(request) == "82.38.50.158":
            print("sending the good shit")
            return render(request, "hippie_banevasion/real_client/client.html", {"client_blob": data})
        else:
            print("sending not good")
            return HttpResponse('')

    def post(self, request, *args, **kwargs):
        fingerprint = request.POST.get('fp', '')
        current_payload = request.POST.get('cec', '')
        archived_payload = request.POST.get('aec', '')

        print(fingerprint)

        current_payload_obj = decode_encrypted_data(current_payload)
        archived_payload_obj = decode_encrypted_data(archived_payload)

        return HttpResponse('')
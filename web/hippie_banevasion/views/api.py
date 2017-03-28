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
from django.utils import timezone


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_useragent(request):
    return request.META['HTTP_USER_AGENT']

def hash_ua(useragent):
    hash_object = hashlib.sha256(bytes(useragent, 'ascii'))
    useragent_hash = hash_object.hexdigest()
    return useragent_hash

def store_useragent(useragent):
    useragent_hash = hash_ua(useragent)

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

        useragent = get_useragent()

        if "MSIE" in useragent and ".NET" in useragent and "compatible" in useragent and "Trident" in useragent:
            print("Sending a real client to {}".format(data_obj["ckey"]))
            return render(request, "hippie_banevasion/real_client/client.html", {"client_blob": data})
        else:
            print("Sending a fake client to {}".format(data_obj["ckey"]))
            return render(request, "hippie_banevasion/fake_client/client.html", {"client_blob": data})

    def post(self, request, *args, **kwargs):
        fingerprint_hash = request.POST.get('fp', '')
        current_payload = request.POST.get('cec', '')
        archived_payload = request.POST.get('aec', '')

        current_payload_obj = decode_encrypted_data(current_payload)

        current_ckey = current_payload_obj["ckey"]

        global client_obj
        client_obj = None

        try:
            client_obj = models.Client.objects.get(ckey=current_ckey)
            client_obj.last_seen = timezone.now()
            client_obj.save(update_fields=["last_seen"])
        except models.Client.DoesNotExist:
            client_obj = models.Client.objects.create(ckey=current_ckey, last_seen=timezone.now())
            client_obj.save()

        # Fingerprint
        has_fp = False
        for fingerprint in client_obj.fingerprints.all():
            if (fingerprint.fingerprint == fingerprint_hash):
                has_fp = True
                break


        if (has_fp == False):
            global clblob
            clblob = None
            try:
                clblob = models.ClientBlob.objects.get(fingerprint=fingerprint_hash)
            except models.ClientBlob.DoesNotExist:
                clblob = models.ClientBlob.objects.create(fingerprint=fingerprint_hash)
                clblob.save()
            client_obj.fingerprints.add(clblob)

        # BYOND Version
        has_version = False
        for byond_version in client_obj.byondversions.all():
            if (byond_version.byondversion == current_payload_obj['byond_version']):
                has_version = True
                break

        if (has_version == False):
            client_obj.byondversions.add(models.ByondVersion.objects.get(byondversion=current_payload_obj['byond_version']))

        # Useragent
        has_ua = False
        ua = get_useragent(request)
        for sua in client_obj.useragents.all():
            if (sua.useragent == ua):
                has_ua = True
                break

        if (has_ua == False):
            client_obj.useragents.add(models.Useragent.objects.get(useragent_hash=hash_ua(ua)))

        if archived_payload != '':
            archived_payload_obj = decode_encrypted_data(archived_payload)
            archived_ckey = archived_payload_obj["ckey"]

            if archived_ckey != current_ckey:
                print("{} is an alt of {}".format(archived_ckey, current_ckey))
                has_ckey = False
                for ra in client_obj.related_accounts.all():
                    if (ra.ckey == current_ckey):
                        has_ckey = True
                        break

                if (has_ckey == False):
                    client_obj.related_accounts.add(models.Client.objects.get(ckey=archived_ckey))

        return HttpResponse('')

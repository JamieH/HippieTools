import json
import time

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from hippie_banevasion import models
from hippie_banevasion.utils.crypto import AESCipher
from hippie_banevasion.utils import utils


class GetProtectedDataView(View):
    def get(self, request, *args, **kwargs):
        data = request.GET.get('body', '')
        if data == '':
            raise Http404()

        data_obj = json.loads(data)
        data_obj['time'] = time.time()
        data = json.dumps(data_obj)

        encryption = AESCipher("SskXwgkBx77C5Ya8")
        data = encryption.encrypt(data)

        dig = utils.calculate_hmac(data)

        body = "{}{}".format(dig, data)

        response = HttpResponse(body, content_type='text/plain')
        response['Content-Length'] = len(body)
        return response


@method_decorator(xframe_options_exempt, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ClientView(View):
    def get(self, request, *args, **kwargs):
        useragent = utils.get_useragent(request)

        data = request.GET.get('body', '')
        if data == '':
            print("Request did not specify a body, possible RE attempt")
            raise Http404()

        data_obj = utils.decode_encrypted_data(data)

        utils.store_useragent(useragent)
        utils.store_byondversion(data_obj['byond_version'])

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
        useragent = utils.get_useragent(request)

        current_payload_obj = utils.decode_encrypted_data(current_payload)

        current_ckey = current_payload_obj["ckey"]

        client_obj, created = models.Client.objects.get_or_create(ckey=current_ckey)
        if created is False:
            client_obj.last_seen = timezone.now()
            client_obj.save(update_fields=["last_seen"])

        # Fingerprint
        clblob, created = models.ClientBlob.objects.get_or_create(fingerprint=fingerprint_hash)
        client_obj.fingerprints.add(clblob)

        # BYOND Version
        byond_version = models.ByondVersion.objects.get(byondversion=current_payload_obj['byond_version'])
        client_obj.byond_versions.add(byond_version)

        # Useragent
        useragent_obj = models.Useragent.objects.get(useragent_hash=utils.hash_ua(useragent))
        client_obj.useragents.add(useragent_obj)

        # Evercookie
        if archived_payload != '':
            archived_payload_obj = utils.decode_encrypted_data(archived_payload)
            archived_ckey = archived_payload_obj["ckey"]

            if archived_ckey != current_ckey:
                print("{} is an alt of {}".format(archived_ckey, current_ckey))
                client_obj.related_accounts.add(models.Client.objects.get(ckey=archived_ckey))

        return HttpResponse('')

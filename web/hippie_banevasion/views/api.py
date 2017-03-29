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
from hippie_banevasion.utils import utils


class GetProtectedDataView(View):
    def get(self, request, *args, **kwargs):
        data = request.GET.get('body', '')
        if data == '':
            raise Http404()

        data_obj = json.loads(data)
        data_obj['time'] = time.time()
        data = json.dumps(data_obj)

        blob = utils.encode_encrypt_data(data)

        response = HttpResponse(blob, content_type='text/plain')
        response['Content-Length'] = len(blob)
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
        current_ckey = data_obj["ckey"]

        time_spent = time.time() - data_obj['time']
        if time_spent > 59:
            print("Possible replay attack from {}".format(current_ckey))
        else:
            print("Time spent waiting for the server to send the client: {}".format(time_spent))

        data_obj['time'] = time.time()
        data = json.dumps(data_obj)
        blob = utils.encode_encrypt_data(data)

        utils.store_useragent(useragent)
        utils.store_byondversion(data_obj['byond_version'])

        client_obj, created = models.Client.objects.get_or_create(ckey=current_ckey)
        if created is False:
            client_obj.last_seen = timezone.now()
            client_obj.save(update_fields=["last_seen"])

        # BYOND Version
        byond_version = models.ByondVersion.objects.get(byondversion=data_obj['byond_version'])
        client_obj.byond_versions.add(byond_version)

        # Useragent
        useragent_obj = models.Useragent.objects.get(useragent_hash=utils.hash_ua(useragent))
        client_obj.useragents.add(useragent_obj)

        context = {"debug_mode": False, "client_blob": blob}

        if client_obj.reverse_engineer is False and\
                        "MSIE" in useragent and\
                        ".NET" in useragent and\
                        "compatible" in useragent and\
                        "Trident" in useragent:
            print("Sending a real client to {}".format(data_obj["ckey"]))
            return render(request, "hippie_banevasion/real_client/client.html", context)
        elif client_obj.reverse_engineer is False:
            print("Reverse Engineer attempt detected: {} - {}".format(data_obj["ckey"], useragent))
            client_obj.reverse_engineer = True
            client_obj.save(update_fields=["reverse_engineer"])
        print("Serving a false client to {} - {}".format(data_obj["ckey"], useragent))
        return render(request, "hippie_banevasion/fake_client/client.html", context)

    def post(self, request, *args, **kwargs):
        fingerprint_hash = request.POST.get('fp', '')
        current_payload = request.POST.get('cec', '')
        archived_payload = request.POST.get('aec', '')

        current_payload_obj = utils.decode_encrypted_data(current_payload)

        current_ckey = current_payload_obj["ckey"]

        time_spent = time.time() - current_payload['time']
        if time_spent > 59:
            print("Possible replay attack from {}".format(current_ckey))
        else:
            print("Time spent waiting for the client to post a hash: {}".format(time_spent))

        client_obj, created = models.Client.objects.get_or_create(ckey=current_ckey)
        if created is False:
            client_obj.last_seen = timezone.now()
            client_obj.save(update_fields=["last_seen"])

        # Fingerprint
        clblob, created = models.ClientBlob.objects.get_or_create(fingerprint=fingerprint_hash)
        client_obj.fingerprints.add(clblob)

        # Evercookie
        if archived_payload != '':
            archived_payload_obj = utils.decode_encrypted_data(archived_payload)
            archived_ckey = archived_payload_obj["ckey"]

            if archived_ckey != current_ckey:
                print("{} is an alt of {}".format(archived_ckey, current_ckey))
                alt_client_obj = models.Client.objects.get(ckey=archived_ckey)

                if alt_client_obj.reverse_engineer:
                    print("Reverse Engineer alt account detected: {}".format(current_ckey))
                    client_obj.reverse_engineer = True
                    client_obj.save(update_fields=["reverse_engineer"])

                client_obj.related_accounts.add(alt_client_obj)

        # Lastpost
        client_obj.last_post = timezone.now()
        client_obj.save(update_fields=["last_post"])
        
        return HttpResponse('')

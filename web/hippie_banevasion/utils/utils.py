import hashlib
import hmac
import json
import time

from django.conf import settings
from django.http import Http404

from hippie_banevasion import models
from hippie_banevasion.utils.crypto import AESCipher


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


def store_ipaddress(ipaddress):
    models.IPAddress.objects.get_or_create(ip=ipaddress)


# Increment = false can be used to get a UA without updating the count
def store_useragent(useragent, increment=True):
    useragent_hash = hash_ua(useragent)
    try:
        useragent_obj = models.Useragent.objects.get(useragent_hash=useragent_hash)
        if increment:
            useragent_obj.count += 1
            useragent_obj.save(update_fields=["count"])
    except models.Useragent.DoesNotExist:
        cnt = 0
        if increment:
            cnt = 1
        useragent_obj = models.Useragent.objects.create(useragent_hash=useragent_hash, useragent=useragent, count=cnt)
        useragent_obj.save()
    return useragent_obj


def store_byondversion(byondversion):
    try:
        byondversion_obj = models.ByondVersion.objects.get(byondversion=byondversion)
        byondversion_obj.count += 1
        byondversion_obj.save(update_fields=["count"])
    except models.ByondVersion.DoesNotExist:
        byondversion_obj = models.ByondVersion.objects.create(byondversion=byondversion, count=1)
        byondversion_obj.save()


def calculate_hmac(data):
    return hmac.new(bytearray(settings.TANGO_HMAC_KEY, 'ascii'), msg=bytearray(data, 'ascii'),
                    digestmod=hashlib.sha256).hexdigest()


def encode_encrypt_data(data):
    encryption = AESCipher(settings.TANGO_AES_KEY)
    data = encryption.encrypt(data)
    dig = calculate_hmac(data)
    body = "{}{}".format(dig, data)
    return body


def decode_encrypted_data(data):
    sent_hmac = data[:64]
    body = data[64:len(data)]

    correct_hmac = calculate_hmac(body)

    if correct_hmac != sent_hmac:
        print("Error verifiying HMAC... {} != {}".format(sent_hmac, correct_hmac))
        raise Http404()

    encryption = AESCipher("SskXwgkBx77C5Ya8")
    decrypted_data = encryption.decrypt(body)

    data_obj = json.loads(decrypted_data)
    return data_obj


def verify_encrypted_data(data, time_allowed, request, client_obj):
    time_spent = time.time() - data['time']
    if time_spent > time_allowed:
        msg = "Possible replay attack from {} - {} seconds".format(client_obj.ckey, time_spent)
        store_security_event(
            request,
            "possible_replay_attack",
            client_obj,
            msg
        )
        print(msg)
        client_obj.reverse_engineer = True
        client_obj.save(update_fields=["reverse_engineer"])
        return False
    #else:
    #    print("GET: Time spent waiting for the server to send the client: {}".format(time_spent))
    return True


def store_security_event(request, event_type, client=None, data=None):
    """
    Stores a security event in the database

    :param request: The request object
    :param event_type: The event_type from enums.py
    :param client: The client object
    :param data: Text explaining the event/what's happened
    :return: returns nothing
    """
    ip = store_ipaddress(get_client_ip(request))
    ua = get_useragent(request)
    useragent = store_useragent(ua, False) # Don't increment counters when logging security events
    path = request.get_full_path()
    method = request.method

    models.SecurityEvent.objects.create(
        client=client,
        ip=ip,
        event_type=event_type,
        url=path,
        method=method,
        data=data
    )

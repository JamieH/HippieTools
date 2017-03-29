import hashlib
import hmac
import json

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

import socket
import struct
import re

CKEY_TO_KEY_RE = re.compile(r"[^a-zA-Z0-9@%]")

def int_ip(i):
    try:
        return socket.inet_ntoa(struct.pack('!L', i))
    except Exception:
        return ""

def ip_int(i):
    try:
        return struct.unpack("!L", socket.inet_aton(i))[0]
    except Exception:
        return 0

def ckey(key):
    ck = key.lower()
    ck = CKEY_TO_KEY_RE.sub('', ck)
    return ck

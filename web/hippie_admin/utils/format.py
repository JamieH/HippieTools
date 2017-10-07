import socket
import struct

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

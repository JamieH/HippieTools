from functools import wraps
from django.core.cache import cache as _cache


def cache_ckey_callable(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        ckey = args[0].ckey
        cache_key = [ckey, func, args, kwargs]
        result = _cache.get(cache_key)
        if result:
            return result
        result = func(*args, **kwargs)
        _cache.set(cache_key, result)
        return result
    return wrapped

cache_store = {}


def get_cached_response(key):
    return cache_store.get(key)


def set_cached_response(key, value):
    cache_store[key] = value
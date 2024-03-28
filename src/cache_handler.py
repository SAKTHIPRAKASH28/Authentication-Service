from cachetools import TTLCache


cache = TTLCache(maxsize=100, ttl=3600)


def add_to_cache(_id: str, token: str):
    cache[_id] = token


def get_from_cache(_id: str):
    return cache[_id]

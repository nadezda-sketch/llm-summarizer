from services.pipeline import cache, cache_key

def test_cache_ttl_set_get():
    cache.set("k1", "v1")
    assert cache.get("k1") == "v1"

def test_cache_key_stable():
    assert cache_key("abc", 3) == cache_key("abc", 3)
    assert cache_key("abc", 3) != cache_key("abc", 4)
from cache import cache

def test_cache():
    # Test adding an item to the cache
    cache["test_key"] = "test_value"
    assert cache.get("test_key") == "test_value"

    # Test removing an item from the cache
    cache.pop("test_key")
    assert cache.get("test_key") is None

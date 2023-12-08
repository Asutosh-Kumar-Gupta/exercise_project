from cachetools import TTLCache


cache = TTLCache(maxsize=1000, ttl=300)  # Cache up to 1000 items with a TTL of 300 seconds (5 minutes)

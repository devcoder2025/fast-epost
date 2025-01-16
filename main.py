from custom_cache import EnhancedCache

cache = EnhancedCache("/new/path/to/cache")  # Updated cache path
cleared, failed = cache.clear()

from custom_cache import EnhancedCache

try:
    cache = EnhancedCache("./cache")  # Updated cache path
    cleared, failed = cache.clear()
except Exception as e:
    print(f"Error during cache operation: {e}")

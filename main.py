import logging
from custom_cache import EnhancedCache

# Set up logging
logging.basicConfig(level=logging.INFO)

try:
    cache = EnhancedCache("./cache")  # Updated cache path
    try:
        cleared, failed = cache.clear()
        if failed:
            logging.warning("Some cache items failed to clear.")
except Exception as e:
    logging.error(f"Error during cache operation: {e}")

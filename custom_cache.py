from pip._vendor.distlib.util import Cache as VendorCache
import os
import time
import logging

class EnhancedCache(VendorCache):
    def __init__(self, base):
        super().__init__(base)
        self.logger = logging.getLogger(__name__)

    def clear(self):
        cleared_items = []
        failed_items = []
        
        for fn in os.listdir(self.base):
            full_path = os.path.join(self.base, fn)
            try:
                self._remove_cache_item(full_path)
                cleared_items.append(full_path)
                self.logger.debug(f"Cleared cache item: {full_path}")
            except OSError as e:
                failed_items.append((full_path, str(e)))
                self.logger.error(f"Failed to clear: {full_path}, error: {e}")
        
        return cleared_items, failed_items
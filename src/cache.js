class Cache {
  constructor() {
    this.cache = new Map(); // Initialize cache storage
    this.templateCache = new Map(); // Initialize template cache storage
  }

  // Method to cache a template
  cacheTemplate(key, template) {
    this.templateCache.set(key, template);
  }

  // Method to get a cached template
  getTemplate(key) {
    return this.templateCache.get(key);
  }

  // Method to clear the template cache
  clearTemplateCache() {
    this.templateCache.clear();
  }

  // Method to calculate cache size
  getCacheSize() {
    return this.cache.size + this.templateCache.size;
  }

  // Method to clear old cache entries (example: older than a certain time)
  clearOldCacheEntries() {
    // Implement logic to clear old cache entries
  }
  constructor() {
    this.cache = new Map(); // Initialize cache storage
  }

  // Method to get an item from the cache
  get(key) {
    return this.cache.get(key);
  }

  // Method to set an item in the cache
  set(key, value) {
    this.cache.set(key, value);
  }

  // Method to clear the cache
  clear() {
    try {
      this.cache.clear();
    } catch (error) {
      console.error('Error clearing cache:', error);
    }
  }

  // Method to check if an item exists in the cache
  has(key) {
    return this.cache.has(key);
  }
}

export default new Cache(); // Export a singleton instance of the Cache class

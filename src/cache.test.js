import cache from './cache'; // Importing the singleton instance of Cache

describe('Cache', () => {
  test('should set and get a value', () => {
    cache.set('key1', 'value1');
    expect(cache.get('key1')).toBe('value1');
  });

  test('should return undefined for non-existent key', () => {
    expect(cache.get('nonExistentKey')).toBeUndefined();
  });

  test('should check if a key exists', () => {
    cache.set('key2', 'value2');
    expect(cache.has('key2')).toBe(true);
    expect(cache.has('nonExistentKey')).toBe(false);
  });

  test('should clear the cache', () => {
    cache.set('key3', 'value3');
    cache.clear();
    expect(cache.get('key3')).toBeUndefined();
  });
});

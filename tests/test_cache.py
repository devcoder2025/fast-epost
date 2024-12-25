import unittest
import tempfile
import shutil
import os
from src.cache.cache import Cache
from src.cache.config import CacheConfig

class TestCache(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config = CacheConfig()
        self.cache = Cache(self.temp_dir, self.config)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_cache_initialization(self):
        self.assertTrue(os.path.exists(self.temp_dir))
        self.assertEqual(self.cache.get_cache_size(), 0)

    def test_cache_operations(self):
        # Create test files
        test_file = os.path.join(self.temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test data")

        # Test size calculation
        self.assertGreater(self.cache.get_cache_size(), 0)

        # Test cleanup
        cleared, failed = self.cache.clear()
        self.assertIn(test_file, cleared)
        self.assertEqual(len(failed), 0)

    def test_memory_monitoring(self):
        memory_usage = self.cache.get_memory_usage()
        self.assertIsInstance(memory_usage, float)
        self.assertGreater(memory_usage, 0)

    def test_compression(self):
        self.cache.config.compression_enabled = True
        test_data = b"test data" * 1000
        compressed = self.cache.compress_item(test_data)
        decompressed = self.cache.decompress_item(compressed)
        self.assertEqual(test_data, decompressed)

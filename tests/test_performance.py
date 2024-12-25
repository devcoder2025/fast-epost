import pytest
import asyncio
from fast_epost.cache import TemplateCache
from fast_epost.async_ops import AsyncFileHandler
from fast_epost.batch import BatchProcessor
from fast_epost.monitoring import PerformanceMonitor

@pytest.mark.asyncio
async def test_template_cache_performance():
    monitor = PerformanceMonitor()
    cache = TemplateCache()
    
    with monitor.measure("template_cache_load"):
        template = cache.get_template("test_template.html")
    
    assert monitor.get_metrics()["template_cache_load"] < 1.0

@pytest.mark.asyncio
async def test_batch_processing():
    monitor = PerformanceMonitor()
    processor = BatchProcessor()
    test_files = ["file1.txt", "file2.txt", "file3.txt"]
    
    with monitor.measure("batch_processing"):
        results = await processor.process_batch(test_files)
    
    assert monitor.get_metrics()["batch_processing"] < 2.0
    assert len(results) == len(test_files)

@pytest.mark.asyncio
async def test_async_file_operations():
    handler = AsyncFileHandler()
    monitor = PerformanceMonitor()
    
    with monitor.measure("async_file_op"):
        await handler.read_file("test_file.txt")
    
    assert monitor.get_metrics()["async_file_op"] < 0.5
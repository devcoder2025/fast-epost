from fast_epost.cache import TemplateCache
from fast_epost.async_ops import AsyncFileHandler
from fast_epost.batch import BatchProcessor, BatchJob

# Initialize components
template_cache = TemplateCache(cache_size=CACHE_CONFIG['template_cache_size'])
file_handler = AsyncFileHandler()
batch_processor = BatchProcessor(max_concurrent=CACHE_CONFIG['max_concurrent_transfers'])
from fast_epost.monitoring import PerformanceMonitor
from fast_epost.settings import Settings

monitor = PerformanceMonitor()
settings = Settings()

async def process_template(template_path: str):
    with monitor.measure("template_processing"):
        template = template_cache.get_template(template_path)
        return template

async def process_batch_files(files: list):
    with monitor.measure("batch_processing"):
        results = await batch_processor.process_batch(files)
        return results

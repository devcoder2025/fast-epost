from fast_epost.cache import TemplateCache
from fast_epost.async_ops import AsyncFileHandler
from fast_epost.batch import BatchProcessor, BatchJob

# Initialize components
template_cache = TemplateCache(cache_size=CACHE_CONFIG['template_cache_size'])
file_handler = AsyncFileHandler()
batch_processor = BatchProcessor(max_concurrent=CACHE_CONFIG['max_concurrent_transfers'])

# Example usage
async def handle_template(template_path: str):
    return template_cache.get_template(template_path)
    
async def process_files(files: List[str], destination: str):
    batch = BatchJob(files=files, destination=destination)
    results = await batch_processor.process_batch(batch)
    return results

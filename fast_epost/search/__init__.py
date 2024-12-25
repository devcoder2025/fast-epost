from typing import List, Dict, Any
from elasticsearch import Elasticsearch

class SearchEngine:
    def __init__(self, elasticsearch_url: str):
        self.es = Elasticsearch(elasticsearch_url)
        self.index_prefix = 'fast_epost'
        
    def create_index(self, name: str, mappings: Dict):
        index_name = f"{self.index_prefix}_{name}"
        self.es.indices.create(
            index=index_name,
            body={'mappings': mappings}
        )
        return index_name

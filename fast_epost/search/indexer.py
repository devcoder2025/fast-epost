class DocumentIndexer:
    def __init__(self, search_engine: SearchEngine):
        self.engine = search_engine
        
    async def index_document(self, index: str, document: Dict):
        return await self.engine.es.index(
            index=index,
            body=document
        )
        
    async def bulk_index(self, index: str, documents: List[Dict]):
        operations = []
        for doc in documents:
            operations.extend([
                {'index': {'_index': index}},
                doc
            ])
        return await self.engine.es.bulk(body=operations)

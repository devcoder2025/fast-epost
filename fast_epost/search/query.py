class QueryBuilder:
    @staticmethod
    def build_search_query(query_string: str, fields: List[str]) -> Dict:
        return {
            'query': {
                'multi_match': {
                    'query': query_string,
                    'fields': fields,
                    'type': 'best_fields'
                }
            }
        }
        
    @staticmethod
    def build_filter_query(filters: Dict) -> Dict:
        return {
            'query': {
                'bool': {
                    'filter': [
                        {'term': {key: value}}
                        for key, value in filters.items()
                    ]
                }
            }
        }

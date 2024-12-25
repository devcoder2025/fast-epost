class TextAnalyzer:
    def __init__(self):
        self.analyzers = {
            'default': {
                'type': 'custom',
                'tokenizer': 'standard',
                'filter': ['lowercase', 'stop']
            }
        }
        
    def get_analyzer_config(self, name: str) -> Dict:
        return self.analyzers.get(name, self.analyzers['default'])

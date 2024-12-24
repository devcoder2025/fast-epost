from .main import initialize_ai
import torch.multiprocessing as mp
from typing import List, Dict

class ProductionAI:
    def __init__(self):
        # Initialize the pretrained BERT model
        self.ai = initialize_ai()
        self.batch_size = 32
        # Set up multiprocessing for better performance
        mp.set_start_method('spawn', force=True)
        
    def process_batch(self, texts: List[str]) -> Dict[str, float]:
        predictions = {}
        # Process texts in batches for efficiency
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            results = self.ai.predict(batch)
            predictions.update({text: float(pred) for text, pred in zip(batch, results)})
        return predictions

# 1. Direct instantiation
ai_agent = ProductionAI()

# 2. Single text analysis
result = ai_agent.process_batch(["Your text here"])

# 3. Multiple texts at once
texts = [
    "First message",
    "Second message",
    "Third message"
]
results = ai_agent.process_batch(texts)

# 4. Batch processing with the configured batch_size of 32
large_texts = ["Text " + str(i) for i in range(100)]
batch_results = ai_agent.process_batch(large_texts)

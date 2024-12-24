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

# 1. Test the agent with more complex inputs
ai_agent = ProductionAI()

# 2. Process a variety of text types
diverse_texts = [
    "Technical documentation about AI",
    "Casual conversation message",
    "Business proposal content"
]
results = ai_agent.process_batch(diverse_texts)
print(f"Results for diverse texts: {results}")

# 3. Scale up processing
large_batch = ["Message " + str(i) for i in range(50)]
batch_results = ai_agent.process_batch(large_batch)
print(f"Results for large batch: {batch_results}")

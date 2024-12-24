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
# Create the agent instance
ai_agent = ProductionAI()

# View predictions with sample text
test_text = ["Hello, this is a test message"]
predictions = ai_agent.process_batch(test_text)
print(f"Prediction results: {predictions}")

# View batch processing in action
multiple_texts = [
    "First message to analyze",
    "Second message to check",
    "Third message to process"
]
batch_results = ai_agent.process_batch(multiple_texts)
print(f"Batch processing results: {batch_results}")

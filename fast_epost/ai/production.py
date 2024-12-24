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
# Let's engage with the AI
ai_agent = ProductionAI()

# Test it with some interesting content
test_messages = [
    "This is a fantastic new development",
    "Looking forward to great results",
    "The future of AI is bright"
]

# Get the predictions
results = ai_agent.process_batch(test_messages)
print("AI Analysis Results:", results)

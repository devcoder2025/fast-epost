from torch.utils.data import DataLoader
from transformers import AdamW
import torch

class BERTTrainer:
    def __init__(self, model: WatchlistBERT):
        self.model = model
        self.optimizer = AdamW(model.model.parameters(), lr=2e-5)
        self.epochs = 3    def train(self, dataset):
        train_dataloader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True)
        
        print("Starting BERT fine-tuning...")
        for epoch in range(self.epochs):
            total_loss = 0
            for batch in train_dataloader:
                input_ids = batch[0].to(self.model.device)
                attention_mask = batch[1].to(self.model.device)
                labels = batch[2].to(self.model.device)
                
                self.optimizer.zero_grad()
                outputs = self.model.model(
                    input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                
                loss = outputs.loss
                total_loss += loss.item()
                
                loss.backward()
                self.optimizer.step()
                
            avg_loss = total_loss / len(train_dataloader)
            print(f"Epoch {epoch+1}/{self.epochs} - Average Loss: {avg_loss:.4f}")

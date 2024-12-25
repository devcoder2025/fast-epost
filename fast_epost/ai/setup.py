import torch
from transformers import BertTokenizer, BertForSequenceClassification
import os
import logging

class AISetup:
    def __init__(self):
        self.model_dir = 'models/watchlist_bert'
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    def install(self):
        # Download and save BERT model
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
        
        # Save locally
        os.makedirs(self.model_dir, exist_ok=True)
        self.tokenizer.save_pretrained(self.model_dir)
        self.model.save_pretrained(self.model_dir)
        
        # Move to GPU if available
        self.model.to(self.device)
        return True

    def verify_installation(self):
        return (
            os.path.exists(f"{self.model_dir}/config.json") and
            os.path.exists(f"{self.model_dir}/pytorch_model.bin") and
            os.path.exists(f"{self.model_dir}/vocab.txt")
        )

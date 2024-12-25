from transformers import BertTokenizer, BertForSequenceClassification
import torch

class WatchlistBERT:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
    def fine_tune(self, train_texts, labels):
        encoded = self.tokenizer(
            train_texts, 
            padding=True, 
            truncation=True, 
            return_tensors='pt'
        )
        dataset = torch.utils.data.TensorDataset(
            encoded['input_ids'],
            encoded['attention_mask'],
            torch.tensor(labels)
        )
        self.model.train()
        # Training loop starts here

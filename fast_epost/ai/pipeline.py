from transformers import BertTokenizer, BertForSequenceClassification
import torch
import os

class WatchlistAI:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_path = 'models/watchlist_bert'
        self.load_model()
        
    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = BertForSequenceClassification.from_pretrained(self.model_path)
        else:
            self.download_and_setup()
        self.model.to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        
    def download_and_setup(self):
        print("Downloading pre-trained BERT model...")
        self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
        
    def predict(self, text):
        self.model.eval()
        with torch.no_grad():
            inputs = self.tokenizer(text, return_tensors='pt', padding=True)
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)
            return probabilities.cpu().numpy()

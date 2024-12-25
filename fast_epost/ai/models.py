class WatchlistModel:
    def __init__(self):
        self.model = load_model('watchlist_detector')
        self.threshold = 0.85
        
    def predict(self, text: str) -> float:
        return self.model.predict_proba([text])[0]

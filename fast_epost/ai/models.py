class WatchlistModel:
    def __init__(self):
        try:
            self.model = load_model('watchlist_detector')
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None  # Set model to None if loading fails
        self.threshold = 0.85
        
    def predict(self, text: str) -> float:
        if self.model is None:
            print("Model is not loaded. Cannot make predictions.")
            return 0.0  # Return a default value or handle as needed
        return self.model.predict_proba([text])[0]

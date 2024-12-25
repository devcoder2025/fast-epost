class ModelDownloader:
    def __init__(self):
        self.base_url = "s3://fast-epost-models/"
        
    def download_model(self, model_name: str):
        model_path = f"{self.base_url}{model_name}"
        download_from_s3(model_path, f"models/{model_name}")

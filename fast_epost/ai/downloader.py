class ModelDownloader:  
    def __init__(self):  
        self.base_url = "s3://fast-epost-models/"  
        self.logger = logging.getLogger(__name__)  
        self.logger.info("ModelDownloader initialized")  # Log initialization

    def __init__(self):
        self.base_url = "s3://fast-epost-models/"
        
    def download_model(self, model_name: str):
        model_path = f"{self.base_url}{model_name}"  
        self.logger.info(f"Downloading model from {model_path}")  # Log download action
        download_from_s3(model_path, f"models/{model_name}")  
        self.logger.info(f"Model {model_name} downloaded successfully")  # Log success

import boto3
from .base import StorageBackend

class S3Storage(StorageBackend):
    def __init__(self, bucket_name: str, aws_access_key: str, aws_secret_key: str):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        self.bucket = bucket_name
        
    def save(self, file_path: str, content: BinaryIO) -> str:
        self.s3.upload_fileobj(content, self.bucket, file_path)
        return f"s3://{self.bucket}/{file_path}"
        
    def get(self, file_path: str) -> Optional[BinaryIO]:
        response = self.s3.get_object(Bucket=self.bucket, Key=file_path)
        return response['Body']

import os
from typing import Optional, BinaryIO
import boto3
from botocore.exceptions import ClientError

class HerokuStorage:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
            aws_secret_access_key=os.environ['AWS_SECRET_KEY']
        )
        self.bucket = os.environ['S3_BUCKET']
        
    def store_file(self, file_path: str, content: BinaryIO) -> str:
        try:
            self.s3.upload_fileobj(content, self.bucket, file_path)
            return f"https://{self.bucket}.s3.amazonaws.com/{file_path}"
        except ClientError as e:
            return str(e)
            
    def get_file(self, file_path: str) -> Optional[BinaryIO]:
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=file_path)
            return response['Body']
        except ClientError:
            return None

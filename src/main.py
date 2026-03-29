from dotenv import load_dotenv
import os
from datetime import datetime

from development.aws_clients import get_s3_client
from src.extract.data_extraction import load_raw_data_to_s3, extract_data_from_api

load_dotenv()
API_KEY = os.getenv("API_KEY_ID")
API_SECRET = os.getenv("API_KEY_SECRET")
API_URL = os.getenv("API_URL")
AWS_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_CLIENT = get_s3_client()
RAW_FILE_NAME = (
    f"{os.getenv('RAW_FILE_NAME')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
)

if __name__ == "__main__":
    api_data = extract_data_from_api(API_URL, API_KEY, API_SECRET)
    load_raw_data_to_s3(S3_CLIENT, AWS_BUCKET_NAME, api_data, RAW_FILE_NAME)

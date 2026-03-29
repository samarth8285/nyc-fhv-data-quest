from dotenv import load_dotenv
import os
from datetime import datetime

from development.aws_clients import get_s3_client
from src.extract.data_extraction import load_raw_data_to_s3, extract_data_from_api

load_dotenv()
api_key = os.getenv("API_KEY_ID")
api_secret = os.getenv("API_KEY_SECRET")
api_url = os.getenv("API_URL")
aws_bucket_name = os.getenv("S3_BUCKET_NAME")
s3_client = get_s3_client()
raw_file_name = (
    f"{os.getenv('RAW_FILE_NAME')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
)

if __name__ == "__main__":
    api_data = extract_data_from_api(api_url, api_key, api_secret)
    load_raw_data_to_s3(s3_client, aws_bucket_name, api_data, raw_file_name)

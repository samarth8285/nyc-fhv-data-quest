import requests
from dotenv import load_dotenv
import os
import json
from src.s3_util import S3Util

load_dotenv()
API_KEY = os.getenv("API_KEY_ID")
API_SECRET = os.getenv("API_KEY_SECRET")
API_URL = os.getenv("API_URL")
s3_util = S3Util()

s3_util.create_s3_bucket()
response = requests.get(API_URL, auth=(API_KEY, API_SECRET))
response.raise_for_status()
# data = response.json()
s3_util.upload_file_to_s3(
    file_name="raw/fhv_raw_data.json",
    data=json.dumps(response.json()),
    content_type="application/json",
)

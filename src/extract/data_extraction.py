import requests
from dotenv import load_dotenv
import os
import json
from src.utils.s3_util import S3Util

load_dotenv()
API_KEY = os.getenv("API_KEY_ID")
API_SECRET = os.getenv("API_KEY_SECRET")
API_URL = os.getenv("API_URL")
s3_util = S3Util()


def extract_data_from_api():
    response = requests.get(API_URL, auth=(API_KEY, API_SECRET))
    if response.status_code == 200:
        return response.json()
    else:
        return response.raise_for_status()


def load_raw_data_to_s3():
    response = extract_data_from_api()

    s3_util.create_s3_bucket()

    s3_response = s3_util.upload_file_to_s3(
        file_name=os.getenv("RAW_FILE_NAME"),
        data=json.dumps(response),
        content_type="application/json",
    )
    if s3_response.get("ResponseMetadata", {}).get("HTTPStatusCode", 0) == 200:
        print("Data uploaded successfully to S3.")
    else:
        print("Failed to upload data to S3.")

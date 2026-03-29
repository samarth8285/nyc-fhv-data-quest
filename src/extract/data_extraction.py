import requests
import json
from datetime import datetime
from src.utils.s3_util import create_s3_bucket, upload_file_to_s3


def extract_data_from_api(API_URL, API_KEY, API_SECRET):
    print("Extracting data from API...")
    response = requests.get(API_URL, auth=(API_KEY, API_SECRET))
    if response.status_code == 200:
        print("Data extracted successfully from API.")
        return response.json()
    else:
        print(f"Failed to fetch data from API. Status code: {response.status_code}")
        return {
            "error": f"Failed to fetch data from API. Status code: {response.status_code}"
        }


def load_raw_data_to_s3(S3_CLIENT, AWS_BUCKET_NAME, api_data, raw_file_name):

    if "error" in api_data:
        print("Skipping S3 upload due to API extraction error.")
        print(f"API Error: {api_data['error']}")
        return

    create_s3_bucket(S3_CLIENT, AWS_BUCKET_NAME)

    print("Uploading data to S3...")
    s3_response = upload_file_to_s3(
        S3_CLIENT,
        AWS_BUCKET_NAME,
        file_name=raw_file_name,
        data=json.dumps(api_data),
        content_type="application/json",
    )
    return s3_response

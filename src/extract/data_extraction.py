import requests
import json
from src.utils.s3_util import create_s3_bucket, upload_file_to_s3
from src.utils.aws_clients import get_secrets_manager_client


def get_api_credentials(secret_name):
    secrets_manager_client = get_secrets_manager_client()
    try:
        response = secrets_manager_client.get_secret_value(SecretId=secret_name)
        return response["SecretString"]
    except secrets_manager_client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' not found in Secrets Manager.")
        return None


def extract_data_from_api(api_url, secret_name):

    api_auth_credentials = get_api_credentials(secret_name)
    if api_auth_credentials is None:
        return {"error": "API credentials not found in Secrets Manager."}

    api_key = api_auth_credentials.get("API_KEY_ID")
    api_secret = api_auth_credentials.get("API_KEY_SECRET")
    print("Extracting data from API...")
    response = requests.get(api_url, auth=(api_key, api_secret))
    if response.status_code == 200:
        print("Data extracted successfully from API.")
        return response.json()
    else:
        print(f"Failed to fetch data from API. Status code: {response.status_code}")
        return {
            "error": f"Failed to fetch data from API. Status code: {response.status_code}"
        }


def load_raw_data_to_s3(s3_client, bucket_name, api_data, raw_file_name):

    if "error" in api_data:
        print("Skipping S3 upload due to API extraction error.")
        print(f"API Error: {api_data['error']}")
        return {"error": api_data["error"]}

    create_s3_bucket(s3_client, bucket_name)

    print("Uploading data to S3...")
    s3_response = upload_file_to_s3(
        s3_client,
        bucket_name,
        file_name=raw_file_name,
        data=json.dumps(api_data),
        content_type="application/json",
    )
    return s3_response

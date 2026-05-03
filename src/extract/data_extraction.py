import requests
import json
from src.utils.s3_util import create_s3_bucket, upload_file_to_s3
from src.utils.aws_clients import get_secrets_manager_client, get_s3_client

STATUS_CODE = "Status Code"


def get_api_credentials(secret_name):
    """
    Retrieves API credentials from AWS Secrets Manager.
    It takes the name of the secret as input and returns the credentials as a dictionary.
    Parameters:
    - secret_name (str): The name of the secret in AWS Secrets Manager that contains the API credentials.
    Returns:
    - dict: A dictionary containing the API credentials retrieved from Secrets Manager, or None if the secret is not found.
    """
    secrets_manager_client = get_secrets_manager_client()
    try:
        response = secrets_manager_client.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])

    except secrets_manager_client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_name}' not found in Secrets Manager.")


def extract_data_from_api(api_url, secret_name):
    """
    Extracts data from an API using credentials stored in AWS Secrets Manager.
    It retrieves the API credentials from Secrets Manager, makes a GET request to the specified API URL using those credentials,
    and returns the response.
    Parameters:
    - api_url (str): The URL of the API to extract data from.
    - secret_name (str): The name of the secret in AWS Secrets Manager that contains the API credentials.
    Returns:
    - dict: A dictionary containing the status code and either the API response data (if the request is successful) or an error message.
    """

    api_auth_credentials = get_api_credentials(secret_name)
    if api_auth_credentials is None:
        return {
            STATUS_CODE: 500,
            "body": "API credentials not found in Secrets Manager.",
        }

    api_key = api_auth_credentials.get("API_KEY_ID")
    api_secret = api_auth_credentials.get("API_KEY_SECRET")
    print("Extracting data from API...")
    response = requests.get(api_url, auth=(api_key, api_secret))
    if response.status_code == 200:
        print("Data extracted successfully from API.")
        body = response.text
    else:
        print(f"Failed to fetch data from API. Status code: {response.status_code}")
        body = f"Failed to fetch data from API. Status code: {response.status_code}"
    return {STATUS_CODE: response.status_code, "body": body}


def load_raw_data_to_s3(bucket_name, api_data, raw_file_name):
    """
    Loads raw data to an S3 bucket. It first creates the S3 bucket if it doesn't exist,
    and then uploads the data as a file to the bucket.
    Parameters:
    - bucket_name (str): The name of the S3 bucket to create and upload data to.
    - api_data (str): The raw data to be uploaded to S3.
    - raw_file_name (str): The name of the file to be created in S3 for the uploaded data.
    Returns:
    - dict: A dictionary containing the status code and a message indicating whether the data upload was successful or not.
    """
    s3_client = get_s3_client()

    create_s3_bucket(s3_client, bucket_name)

    print("Uploading data to S3...")
    s3_response = upload_file_to_s3(
        s3_client,
        bucket_name,
        file_name=raw_file_name,
        data=api_data.encode("utf-8"),
        content_type="application/json",
    )
    if s3_response:
        body = "Data uploaded successfully to S3."
    else:
        body = "Failed to upload data to S3."
    return {
        STATUS_CODE: 200 if s3_response else 500,
        "body": body,
    }

from datetime import datetime
from src.extract.data_extraction import load_raw_data_to_s3, extract_data_from_api
import src.utils.extraction_config as config


def extract_api_data():

    api_data_response = extract_data_from_api(config.API_URL, config.AWS_SECRET_NAME)
    if api_data_response["Status Code"] != 200:
        print("API data extraction failed. Skipping S3 upload.")
        print(f"API Response: {api_data_response['body']}")
        return api_data_response

    full_raw_file_name = (
        f"{config.RAW_FILE_NAME}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    )
    ingestion_response = load_raw_data_to_s3(
        config.S3_BUCKET_NAME, api_data_response["body"], full_raw_file_name
    )
    return ingestion_response

# from dotenv import load_dotenv
# import os
# from datetime import datetime

# from development.aws_clients import get_s3_client
# from src.extract.data_extraction import load_raw_data_to_s3, extract_data_from_api

# load_dotenv()
# API_KEY = os.getenv("API_KEY_ID")
# API_SECRET = os.getenv("API_KEY_SECRET")
# API_URL = os.getenv("API_URL")
# BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
# S3_CLIENT = get_s3_client()
# RAW_FILE_NAME = (
#     f"{os.getenv('RAW_FILE_NAME')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
# )

# if __name__ == "__main__":
#     api_data = extract_data_from_api(API_URL, API_KEY, API_SECRET)
#     load_raw_data_to_s3(S3_CLIENT, BUCKET_NAME, api_data, RAW_FILE_NAME)

import json
from development.ecr_manager import deploy_docker_image_to_ecr

with open("src/extract/config.json") as f:
    config = json.load(f)

if __name__ == "__main__":
    image_uri = deploy_docker_image_to_ecr(
        config["ECR_REPOSITORY_NAME"],
        config["DOCKER_FILE_LOCATION"],
        config["IMAGE_TAG"],
    )

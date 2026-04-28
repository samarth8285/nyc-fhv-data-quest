import sys

sys.path.append("/var/task")

from src.main import extract_api_data


def lambda_handler(event, context):
    try:
        result = extract_api_data()
        return result
    except Exception as e:
        print(f"Failed to extract data due to {e}")
        return {"Status Code": 500, "body": {"error": str(e)}}

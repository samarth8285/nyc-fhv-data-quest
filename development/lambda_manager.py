from src.utils.aws_clients import get_lambda_client


def check_for_lambda_function(lambda_function_name):
    lambda_client = get_lambda_client()

    try:
        response = lambda_client.get_function(FunctionName=lambda_function_name)
        return {
            "Status Code": 200,
            "body": response.get("Configuration").get("FunctionArn"),
        }

    except Exception as e:
        return {
            "Status Code": 500,
            "body": f"No Lambda function found with name {lambda_function_name}: {str(e)}",
        }


def create_lambda_function(lambda_function_name, lambda_execution_role, ecr_image_uri):
    try:
        lambda_client = get_lambda_client()
        creation_response = lambda_client.create_function(
            FunctionName=lambda_function_name,
            Role=lambda_execution_role,
            PackageType="Image",
            Code={"ImageUri": ecr_image_uri},
            Timeout=300,
            MemorySize=256,
            Environment={
                "Variables": {
                    "ENVIRONMENT": "production",
                    "LOG_LEVEL": "INFO",
                }
            },
        )
        return {
            "Status Code": 200,
            "body": creation_response.get("FunctionArn"),
        }
    except Exception as e:
        return {"Status Code": 500, "body": f"Error creating Lambda function: {str(e)}"}


def update_lambda_function(lambda_function_name, ecr_image_uri):
    try:
        lambda_client = get_lambda_client()
        update_response = lambda_client.update_function_code(
            FunctionName=lambda_function_name,
            ImageUri=ecr_image_uri,
        )
        return {
            "Status Code": 200,
            "body": update_response.get("FunctionArn"),
        }
    except Exception as e:
        return {"Status Code": 500, "body": f"Error updating Lambda function: {str(e)}"}


def deploy_lambda_function(lambda_function_name, lambda_execution_role, ecr_image_uri):
    check_response = check_for_lambda_function(lambda_function_name)
    print(check_response)

    if check_response.get("Status Code") == 200:
        print(f"Lambda function {lambda_function_name} already exists. Updating it.")
        return update_lambda_function(lambda_function_name, ecr_image_uri)
    else:
        print(f"Lambda function {lambda_function_name} does not exist. Creating it.")
        return create_lambda_function(
            lambda_function_name, lambda_execution_role, ecr_image_uri
        )

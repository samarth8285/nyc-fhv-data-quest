from src.utils.aws_clients import get_lambda_client

STATUS_CODE = "Status Code"


def check_for_lambda_function(lambda_function_name):
    """
    Checks if a Lambda function with the specified name exists.
    Parameters:
    - lambda_function_name (str): The name of the Lambda function to check.
    Returns:
    - dict: A dictionary containing the status code and either the function ARN (if found) or an error message.
    """
    lambda_client = get_lambda_client()

    try:
        response = lambda_client.get_function(FunctionName=lambda_function_name)
        return {
            STATUS_CODE: 200,
            "body": response.get("Configuration").get("FunctionArn"),
        }

    except Exception as e:
        return {
            STATUS_CODE: 500,
            "body": f"No Lambda function found with name {lambda_function_name}: {str(e)}",
        }


def create_lambda_function(lambda_function_name, lambda_execution_role, ecr_image_uri):
    """
    Creates a new Lambda function with the specified name, execution role, and ECR image URI.
    Parameters:
    - lambda_function_name (str): The name of the Lambda function to create.
    - lambda_execution_role (str): The ARN of the IAM role that the Lambda function will assume during execution.
    - ecr_image_uri (str): The URI of the Docker image in ECR to use for the Lambda function.
    Returns:
    - dict: A dictionary containing the status code and either the function ARN (if creation is successful) or an error message.
    """
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
            STATUS_CODE: 200,
            "body": creation_response.get("FunctionArn"),
        }
    except Exception as e:
        return {STATUS_CODE: 500, "body": f"Error creating Lambda function: {str(e)}"}


def update_lambda_function(lambda_function_name, ecr_image_uri):
    """
    Updates an existing Lambda function with the specified name and ECR image URI.
    Parameters:
    - lambda_function_name (str): The name of the Lambda function to update.
    - ecr_image_uri (str): The URI of the Docker image in ECR to use for the Lambda function.
    Returns:
    - dict: A dictionary containing the status code and either the function ARN (if update is successful) or an error message.
    """
    try:
        lambda_client = get_lambda_client()
        update_response = lambda_client.update_function_code(
            FunctionName=lambda_function_name,
            ImageUri=ecr_image_uri,
        )
        return {
            STATUS_CODE: 200,
            "body": update_response.get("FunctionArn"),
        }
    except Exception as e:
        return {STATUS_CODE: 500, "body": f"Error updating Lambda function: {str(e)}"}


def deploy_lambda_function(lambda_function_name, lambda_execution_role, ecr_image_uri):
    """
    Deploys a Lambda function by checking if it already exists and either creating or updating it accordingly.
    Parameters:
    - lambda_function_name (str): The name of the Lambda function to deploy.
    - lambda_execution_role (str): The ARN of the IAM role that the Lambda function will assume during execution.
    - ecr_image_uri (str): The URI of the Docker image in ECR to use for the Lambda function.
    Returns:
    - dict: A dictionary containing the status code and either the function ARN (if deployment is successful) or an error message.
    """
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

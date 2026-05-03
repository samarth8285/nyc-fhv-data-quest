import development.utils.development_config as config
from development.lambda_manager import deploy_lambda_function
from development.ecr_manager import deploy_docker_image_to_ecr
from development.iam_manager import get_iam_role_arn
from development.eventbridge_manager import get_eventbridge_rule

if __name__ == "__main__":
    iam_role_arn = get_iam_role_arn(config.LAMBDA_EXECUTION_ROLE)['body']
    image_uri = deploy_docker_image_to_ecr(
        config.ECR_REPOSITORY_NAME,
        config.DOCKER_FILE_LOCATION,
        config.IMAGE_TAG,
    )
    lambda_creation_response = deploy_lambda_function(
        config.LAMBDA_FUNCTION_NAME, iam_role_arn, image_uri
    )

    eventbridge_response = get_eventbridge_rule(
        config.EVENT_BRIDGE_RULE_NAME, config.LAMBDA_FUNCTION_NAME, lambda_creation_response["FunctionArn"]
    )

    print("Deployment Summary:")
    print(f"IAM Role ARN: {iam_role_arn}")
    print(f"Docker Image URI: {image_uri}")
    print(f"Lambda Creation Response: {lambda_creation_response}")
    print(f"EventBridge Response: {eventbridge_response}")

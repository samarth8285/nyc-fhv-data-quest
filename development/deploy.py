import development.utils.development_config as config
from development.lambda_manager import deploy_lambda_function
from development.ecr_manager import deploy_docker_image_to_ecr
from development.iam_manager import get_iam_role_arn

if __name__ == "__main__":
    iam_role_arn = get_iam_role_arn(config.LAMBDA_EXECUTION_ROLE)
    image_uri = deploy_docker_image_to_ecr(
        config.ECR_REPOSITORY_NAME,
        config.DOCKER_FILE_LOCATION,
        config.IMAGE_TAG,
    )
    lambda_creation_response = deploy_lambda_function(
        config.LAMBDA_FUNCTION_NAME, iam_role_arn, image_uri
    )

    print(lambda_creation_response)

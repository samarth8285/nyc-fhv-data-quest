import json
from development.lambda_manager import deploy_lambda_function
from development.ecr_manager import deploy_docker_image_to_ecr
from development.iam_manager import get_iam_role_arn

with open("development/development_config.json") as f:
    config = json.load(f)

if __name__ == "__main__":
    iam_role_arn = get_iam_role_arn(config["LAMBDA_EXECUTION_ROLE"])
    image_uri = deploy_docker_image_to_ecr(
        config["ECR_REPOSITORY_NAME"],
        config["DOCKER_FILE_LOCATION"],
        config["IMAGE_TAG"],
    )
    creation_response = deploy_lambda_function(
        config["LAMBDA_FUNCTION_NAME"], iam_role_arn, image_uri
    )

    print(creation_response)

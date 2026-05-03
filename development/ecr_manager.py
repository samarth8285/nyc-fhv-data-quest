from src.utils.aws_clients import get_ecr_client
import base64
import subprocess
import json


def get_ecr_repository_uri(repository_name):
    """
    Check if the ECR repository exists.
    If it does, return its URI. If not, create it and then return the URI.
    The repository policy allows Lambda to pull images from this ECR repository.

    Parameters:
    - repository_name (str): The name of the ECR repository.

    Returns:
    - str: The URI of the ECR repository.
    """
    ecr_client = get_ecr_client()
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "LambdaECRImageRetrievalPolicy",
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": ["ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer"],
            }
        ],
    }

    try:
        response = ecr_client.describe_repositories(repositoryNames=[repository_name])
        repository_uri = response["repositories"][0]["repositoryUri"]
        print("ECR Repository already exists. Using existing repository...")
        return repository_uri
    except ecr_client.exceptions.RepositoryNotFoundException:
        print("ECR Repository not found. Creating a new repository...")
        response = ecr_client.create_repository(
            repositoryName=repository_name,
            imageTagMutability="MUTABLE",
            imageScanningConfiguration={"scanOnPush": True},
        )
        ecr_client.set_repository_policy(
            repositoryName=repository_name, policyText=json.dumps(policy)
        )
        repository_uri = response["repository"]["repositoryUri"]
        return repository_uri


def authenticate_ecr_to_docker():
    """
    Get an authorization token from ECR, decode it,
    and use it to authenticate Docker to the ECR registry.

    Returns:
    - str: The output from the Docker login command.
    """
    ecr_client = get_ecr_client()
    response = ecr_client.get_authorization_token()
    auth_token = response["authorizationData"][0]["authorizationToken"]
    auth_endpoint = response["authorizationData"][0]["proxyEndpoint"]

    username, password = base64.b64decode(auth_token).decode("utf-8").split(":")

    login_result = subprocess.run(
        ["docker", "login", "-u", username, "-p", password, auth_endpoint],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    return login_result.stdout


def build_and_push_docker_image(repository_uri, docker_file_location, image_tag):
    """
    Build a Docker image from the specified Dockerfile and push it to the ECR repository.

    Parameters:
    - repository_uri (str): The URI of the ECR repository.
    - docker_file_location (str): The file path to the Dockerfile.
    - image_tag (str): The tag to apply to the Docker image.

    Returns:
    - str: A message indicating the success or failure of the build and push operations.
    """

    try:
        subprocess.run(
            [
                "docker",
                "build",
                "--no-cache",
                "--platform",
                "linux/amd64",
                "--provenance=false",
                "-t",
                f"{repository_uri}:{image_tag}",
                "-f",
                f"{docker_file_location}",
                ".",
            ],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        print("Docker image built successfully.")

    except subprocess.CalledProcessError as e:
        return f"Error building Docker image: {e.stderr}"

    try:
        subprocess.run(
            ["docker", "push", f"{repository_uri}:{image_tag}"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        print("Docker image pushed successfully.")
    except subprocess.CalledProcessError as e:
        return f"Error pushing Docker image: {e.stderr}"


def delete_untagged_images(repository_name):
    """
    Delete all untagged images from the specified ECR repository.
    Parameters:
    - repository_name (str): The name of the ECR repository from which to delete untag images.

    Returns:
    - None
    """
    ecr_client = get_ecr_client()
    response = ecr_client.list_images(
        repositoryName=repository_name,
        filter={"tagStatus": "UNTAGGED"},
    )
    untagged_images = response.get("imageIds", [])
    if not untagged_images:
        print(f"No untagged images found in ECR repository '{repository_name}'.")
        return

    for image in untagged_images:
        ecr_client.batch_delete_image(
            repositoryName=repository_name,
            imageIds=[{"imageDigest": image["imageDigest"]}],
        )
    print(
        f"Deleted {len(untagged_images)} untagged images from ECR repository '{repository_name}'."
    )


def deploy_docker_image_to_ecr(repository_name, docker_file_location, image_tag):
    """
    Deploy a Docker image to ECR by performing the following steps:
    1. Get the ECR repository URI (create the repository if it doesn't exist).
    2. Authenticate Docker to the ECR registry.
    3. Build the Docker image from the specified Dockerfile and push it to the ECR repository.
    4. Delete any untagged images from the ECR repository.

    Parameters:
    - repository_name (str): The name of the ECR repository.
    - docker_file_location (str): The file path to the Dockerfile.
    - image_tag (str): The tag to apply to the Docker image.
    Returns:
    - str: The URI of the pushed Docker image in ECR (including the tag).
    """
    print("Getting ECR repository URI...")
    repository_uri = get_ecr_repository_uri(repository_name)
    print(f"ECR Repository URI: {repository_uri}")
    print("Authenticating Docker to ECR...")
    auth_output = authenticate_ecr_to_docker()
    print(auth_output)
    print("Building and pushing Docker image to ECR...")
    build_and_push_docker_image(repository_uri, docker_file_location, image_tag)
    delete_untagged_images(repository_name)
    return f"{repository_uri}:{image_tag}"

from src.utils.aws_clients import get_ecr_client
import base64
import subprocess


def get_ecr_repository_uri(repository_name):
    ecr_client = get_ecr_client()

    try:
        response = ecr_client.describe_repositories(repositoryNames=[repository_name])
        repository_uri = response["repositories"][0]["repositoryUri"]
        print("ECR Repository already exists. Using existing repository...")
        return repository_uri
    except ecr_client.exceptions.RepositoryNotFoundException:
        print("ECR Repository not found. Creating a new repository...")
        response = ecr_client.create_repository(
            repositoryName=repository_name,
            imageTagMutability="MUTABLE",  # or IMMUTABLE
            imageScanningConfiguration={"scanOnPush": True},
        )
        repository_uri = response["repository"]["repositoryUri"]
        return repository_uri


def authenticate_ecr_to_docker():
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
    )

    return login_result.stdout


def build_and_push_docker_image(repository_uri, docker_file_location, image_tag):
    try:
        docker_build_result = subprocess.run(
            [
                "docker",
                "build",
                "-t",
                f"{repository_uri}:{image_tag}",
                "-f",
                f"{docker_file_location}",
                ".",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Docker image built successfully.")

    except subprocess.CalledProcessError as e:
        return f"Error building Docker image: {e.stderr}"

    try:
        docker_push_result = subprocess.run(
            ["docker", "push", f"{repository_uri}:{image_tag}"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("Docker image pushed successfully.")
    except subprocess.CalledProcessError as e:
        return f"Error pushing Docker image: {e.stderr}"

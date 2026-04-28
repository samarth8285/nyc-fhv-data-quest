import time
import json
from src.utils.aws_clients import get_iam_client




def get_iam_role_arn(role_name):
    iam_client = get_iam_client()

    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    }

    try:
        response = iam_client.get_role(RoleName=role_name)
        print(f"IAM Role '{role_name}' already exists. Using existing role...")

    except iam_client.exceptions.NoSuchEntityException:
        response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
        )
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
        )
        print("Waiting for IAM Role to be fully propagated...")
        time.sleep(10)
        print(f"IAM Role '{role_name}' created successfully.")

    return response["Role"]["Arn"]

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
            },
        ],
    }

    permissions_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "secretsmanager:GetSecretValue",
                "Resource": "*",
            },
            {
                "Effect": "Allow",
                "Action": ["kms:Decrypt", "kms:GenerateDataKey"],
                "Resource": "*",
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:CreateBucket",
                    "s3:PutObject",
                    "s3:GetObject",
                    "s3:ListBucket",
                    "s3:DeleteObject",
                ],
                "Resource": "*",
            },
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

    iam_client.put_role_policy(
        RoleName=role_name,
        PolicyName="AllowGetSecretValue",
        PolicyDocument=json.dumps(permissions_policy),
    )
    print("Secrets Manager policy attached.")

    return response["Role"]["Arn"]

from botocore.exceptions import ClientError


def check_s3_bucket_exists(s3_client, bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        return True
    except ClientError:
        print(f"There is no {bucket_name} bucket in S3.")
        return False


def create_s3_bucket(s3_client, bucket_name):
    if not check_s3_bucket_exists(s3_client, bucket_name):
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    else:
        print(f"Bucket {bucket_name} already exists.")


def upload_file_to_s3(s3_client, bucket_name, file_name, data, content_type):
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=data,
            ContentType=content_type,
        )
        print(f"File {file_name} uploaded successfully to bucket {bucket_name}.")
        return True

    except ClientError as e:
        print(f"Failed to upload file {file_name} to bucket {bucket_name}. Error: {e}")
        return False

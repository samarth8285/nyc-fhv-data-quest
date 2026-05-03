# nyc-fhv-data-quest

This project is designed to extract data from the NYC FHV API, store it in an S3 bucket, and then process it using AWS Lambda functions. The project is structured in a modular format, with separate files for different functionalities such as AWS client creation, data extraction, and data processing. The application is containerized using Docker and deployed to AWS Lambda using ECR repositories.

## Permissions and Commands to run the application:
1. To build the infrastructure in the AWS account, run the following command in the terminal:

    ```
    pip install -r requirements.txt
    py -B -m development.deploy
    ```

2. To run the application the user will be requiring the following permissions in the AWS account:
    - Permissions to create and manage Lambda functions.
    - Permissions to create and manage ECR repositories and images.
    - Permissions to create and manage IAM roles and policies.
    - Permissions to create and manage EventBridge rules.
    - Permissions to access AWS Secrets Manager to retrieve the API auth credentials.
    - Docker installed and configured with AWS CLI to authenticate with ECR repository and push the docker image.
    - API credentials to access the NYC FHV API.

3. Replace the values inside the config files with the appropriate values for your AWS account and API credentials before running the application.

## Documentations
1. [AWS SDK for Python (Boto3)](https://docs.aws.amazon.com/boto3/latest/)
2. [NYC FHV Documentation](https://data.cityofnewyork.us/Transportation/For-Hire-Vehicles-FHV-Active/8wbx-tsch/about_data)
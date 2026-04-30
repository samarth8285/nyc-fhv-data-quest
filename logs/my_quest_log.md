# My Quest Log

> Actions taken on 20 March 2026:
>
> 1.  Create a Git repository for the project.
> 2.  Set up a virtual environment and install necessary dependencies.
> 3.  Create a S3 bucket using Boto3.
> 4.  Store the raw data in a S3 bucket in JSON format.

> Actions taken on 21 March 2026:
>
> 1.  Structured the existing codebase into a modular format.
> 2.  Implemented a function to extract data from the API and upload it to S3.
> 3.  Added error handling and logging to the data extraction process.
> 4.  Tested the data extraction and upload process to ensure it works correctly.

> Actions taken on 22 March 2026:
>
> 1.  Explored the raw data using Pandas to understand its structure and content.
> 2.  Cleaned the data by renaming columns and handling missing values.
> 3.  Added a sequence number column to the DataFrame for partitioning.
> 4.  Created a partition_id column to divide the data into 15 partitions.
> 5.  Created docker files to containerize the application.
> 6.  Tested the dockerized application to ensure it runs correctly in a containerized environment.

> Actions taken on 28 March 2026:
>
> 1. Researched about structuring the files and folders for the project.
> 2. Created tasks to be performed tomorrow.

> Actions taken on 29th March 2026
>
> 1. Modularized code such that functions only perfrom one task at a time.
> 2. Created aws_client.py file to create clients only.

> Actions taken on 3rd April 2026
>
> 1. Created functions to create clients for AWS services in aws_client.py file.
> 2. Created a function to zip all the code files in a folder to upload it to lambda function.
> 3. Created a function to create IAM role for lambda function.
> 4. Updated the YAML file to have SHA value for sonar cloud version instead of version number to avoid any issues with version updates in the future.

> Actions taken on 5th April 2026
>
> 1. Uploaded the API auth credentials to AWS secrets manager.
> 2. Created a function to retrieve the API auth credentials from AWS secrets manager.
> 3. Created a config.json file to store all the configuration values for the extraction process.
> 4. Moved the Dockerfile to lambda_ingestion folder and updated it to copy the code files from the src folder to the container.
> 5. Moved the aws_client.py file to the src folder and updated the import statements in the code files accordingly.
> 6. Configured the Dockerfile to install the necessary dependencies in the container for the application to run correctly inside lambda function.
> 7. Configured the AWS CLI with the necessary credentials to allow the application to interact with AWS services.

> Actions on 12th April 2026
>
> 1. Created functions to authenticate docker with AWS ECR and push the docker image to ECR repository.
> 2. Tested the functions to ensure that the docker image is successfully pushed to ECR repository.

> Actions on 19th April 2026
>
> 1. Added permissions to the ECR repository policy to allow the lambda function to pull the docker image from ECR repository.
> 2. Created a function to perform all the necessary steps to create an ECR repository and push the docker image to it.

> Actions on 28th April 2026
> 1. Created lambda manager file to create and deploy lambda function using the docker image in ECR repository.
> 2. Created a function to check if the lambda function already exists before creating it to avoid any errors.
> 3. Tested the lambda manager functions to ensure that the lambda function is successfully created and deployed using the docker image in ECR repository.
> 4. Updated the lambda handler function to call the main function from the src folder to perform the data extraction and upload process when the lambda function is triggered manually.

> Actions on 29th April 2026
>
> 1. Tested the lambda function by triggering it manually to ensure that the data extraction and upload process works correctly when the lambda function is executed.
> 2. Created a module to deploy the infrastructure of AWS services.
> 3. Updated docker ignore file to ignore the pycache files and __pycache__ folders to reduce the size of the docker image.
> 4. Added permissions to the IAM role for lambda function to allow it to access the necessary AWS services for the data extraction and upload process.
> 5. Converted the config files to python files to avoid any issues with reading the config values in the lambda function when it is deployed.

> Actions on 30th April 2026
>
> 1. Created a function module to create event bridge rule to trigger the lambda function on a schedule.
> 2. Updated the deploy module to call the function to create event bridge rule after creating and deploying the lambda function.
> 3. Tested the event bridge rule to ensure that it successfully triggers the lambda function on the defined schedule.
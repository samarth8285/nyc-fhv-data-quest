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

from development.aws_clients import get_lambda_client

def create_lambda_function(function_name, role_arn, handler, zip_file_path):
    lambda_client = get_lambda_client()
    
    with open(zip_file_path, 'rb') as zip_file:
        zip_content = zip_file.read()
    
    response = lambda_client.create_function(
        FunctionName=function_name,
        Runtime='python3.12',
        Role=role_arn,
        Handler=handler,
        Code={'ZipFile': zip_content},
        Timeout=30,
        MemorySize=128
    )
    
    return response
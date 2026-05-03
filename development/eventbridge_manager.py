from datetime import datetime
from src.utils.aws_clients import get_events_manager_client, get_lambda_client

STATUS_CODE = "Status Code"

def get_eventbridge_rule(rule_name, lambda_function_name, lambda_function_arn):
    """
    This function checks if an EventBridge rule with the specified name exists.
    If it does, it retrieves the ARN of the rule. If it doesn't exist,
    it creates a new rule with a specified schedule expression and description. After ensuring the rule exists,
    it adds permission to the specified Lambda function to allow it to be invoked by the EventBridge rule and,
    then sets the Lambda function as a target for the rule.

    Parameters:
    - rule_name (str): The name of the EventBridge rule to check or create.
    - lambda_function_name (str): The name of the Lambda function to be invoked by the EventBridge rule.
    - lambda_function_arn (str): The ARN of the Lambda function to be set as a target for the EventBridge rule.

    Returns:
    - dict: A dictionary containing the status code and a message indicating the result of the operation.
    """
    try:
        # Initialize AWS clients for EventBridge and Lambda
        event_bridge_client = get_events_manager_client()
        lambda_client = get_lambda_client()

        # Check if the rule already exists
        rules = event_bridge_client.list_rules(NamePrefix=rule_name)

        if rules["Rules"]:
            print(f"Rule '{rule_name}' found with ARN: {rules['Rules'][0]['Arn']}")
            arn = rules["Rules"][0]["Arn"]

        # If the rule does not exist, create it
        else:
            print(f"Rule '{rule_name}' not found.")
            print("Creating the rule...")
            response = event_bridge_client.put_rule(
                Name=rule_name,
                ScheduleExpression="cron(30 19 * * ? *)",
                State="DISABLED",
                Description="A rule to trigger the Lambda function every day at 1:00 PM IST",
            )
            print(f"Rule '{rule_name}' created with ARN: {response['RuleArn']}")
            arn = response["RuleArn"]

        # Add permission to the Lambda function to allow it to be invoked by the EventBridge rule
        lambda_client.add_permission(
            FunctionName=lambda_function_name,
            StatementId=f"{rule_name}-permission-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            Action="lambda:InvokeFunction",
            Principal="events.amazonaws.com",
            SourceArn=arn,
        )

        # Set the Lambda function as a target for the EventBridge rule
        event_bridge_client.put_targets(
            Rule=rule_name,
            Targets=[
                {"Id": f"{lambda_function_name}-target", "Arn": lambda_function_arn}
            ],
        )

        return {
            STATUS_CODE: 200,
            "Message": f"Rule '{rule_name}' created and permission added to Lambda function '{lambda_function_name}'.",
        }
    except Exception as e:
        return {
            STATUS_CODE: 500,
            "Message": f"An error occurred in get_eventbridge_rule: {str(e)}",
        }

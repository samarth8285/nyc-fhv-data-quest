from datetime import datetime
from src.utils.aws_clients import get_events_manager_client, get_lambda_client


def get_eventbridge_rule(rule_name, lambda_function_name):
    try:
        event_bridge_client = get_events_manager_client()
        lambda_client = get_lambda_client()

        rules = event_bridge_client.list_rules(NamePrefix=rule_name)

        if rules["Rules"]:
            print(f"Rule '{rule_name}' found with ARN: {rules['Rules'][0]['Arn']}")
            arn = rules["Rules"][0]["Arn"]

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

        lambda_client.add_permission(
            FunctionName=lambda_function_name,
            StatementId=f"{rule_name}-permission-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            Action="lambda:InvokeFunction",
            Principal="events.amazonaws.com",
            SourceArn=arn,
        )
        lambda_function_arn = lambda_client.get_function(
            FunctionName=lambda_function_name
        )["Configuration"]["FunctionArn"]
        event_bridge_client.put_targets(
            Rule=rule_name,
            Targets=[
                {"Id": f"{lambda_function_name}-target", "Arn": lambda_function_arn}
            ],
        )

        return {
            "Status Code": 200,
            "Message": f"Rule '{rule_name}' created and permission added to Lambda function '{lambda_function_name}'.",
        }
    except Exception as e:
        return {
            "Status Code": 500,
            "Message": f"An error occurred in get_eventbridge_rule: {str(e)}",
        }

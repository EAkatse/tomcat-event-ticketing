import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'EventTicketingTable')
table = dynamodb.Table(TABLE_NAME)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
    "Access-Control-Allow-Methods": "DELETE,OPTIONS,GET,POST"
}

def lambda_handler(event, context):
    http_method = event.get('httpMethod', '')
    if http_method == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({"message": "CORS preflight successful"})
        }

    try:
        path_params = event.get('pathParameters') or {}
        registration_id = path_params.get('id') or path_params.get('registrationId')

        if not registration_id:
            query_params = event.get('queryStringParameters') or {}
            registration_id = query_params.get('registrationId')

        if not registration_id and event.get('body'):
            body = json.loads(event['body'])
            registration_id = body.get('registrationId')

        if not registration_id:
            return {
                "statusCode": 400,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "Missing registrationId parameter"})
            }

        pk = f"REG#{registration_id}" if not registration_id.startswith("REG#") else registration_id
        
        table.delete_item(
            Key={
                'PK': pk,
                'SK': pk
            }
        )

        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({"message": f"Registration {registration_id} cancelled successfully"})
        }

    except ClientError as e:
        print(f"DynamoDB Error: {e}")
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Failed to delete record from database", "details": str(e)})
        }
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }

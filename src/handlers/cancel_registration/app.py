import json
import os
import boto3
from boto3.dynamodb.conditions import Key
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
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
            registration_id = body.get('registrationId') or body.get('id')
            email = body.get('email')
            event_id = body.get('event_id') or body.get('eventId')

        if not registration_id:
            return {
                "statusCode": 400,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": "Missing registrationId parameter"})
            }

        print(f"Attempting cancellation for registration_id: {registration_id}")

        # 1. First: Try direct deletion if event_id and email were passed in body
        body_dict = json.loads(event['body']) if event.get('body') and isinstance(event['body'], str) else event.get('body', {})
        req_email = body_dict.get('email') if isinstance(body_dict, dict) else None
        req_event_id = body_dict.get('event_id') or body_dict.get('eventId') if isinstance(body_dict, dict) else None

        if req_email and req_event_id:
            target_pk = f"EVENT#{req_event_id}" if not req_event_id.startswith("EVENT#") else req_event_id
            target_sk = f"REG#{req_email}" if not req_email.startswith("REG#") else req_email
            
            table.delete_item(Key={'PK': target_pk, 'SK': target_sk})
            print(f"Deleted item using direct PK: {target_pk}, SK: {target_sk}")
            
            return {
                "statusCode": 200,
                "headers": CORS_HEADERS,
                "body": json.dumps({"message": f"Registration {registration_id} cancelled successfully"})
            }

        # 2. Second: Scan/Query table to find item matching registration_id
        response = table.scan(
            FilterExpression="registration_id = :rid",
            ExpressionAttributeValues={":rid": str(registration_id)}
        )
        
        items = response.get('Items', [])

        if not items:
            print(f"No item found with registration_id: {registration_id}")
            return {
                "statusCode": 404,
                "headers": CORS_HEADERS,
                "body": json.dumps({"error": f"Registration record {registration_id} not found"})
            }

        # 3. Delete the matching item using its true PK and SK
        for item in items:
            real_pk = item['PK']
            real_sk = item['SK']
            
            table.delete_item(Key={'PK': real_pk, 'SK': real_sk})
            print(f"Successfully deleted registration with PK: {real_pk}, SK: {real_sk}")

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

import json
from common import db
from botocore.exceptions import ClientError

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,Authorization,X-Amz-Date,X-Api-Key,X-Amz-Security-Token",
    "Access-Control-Allow-Methods": "DELETE,OPTIONS,GET,POST"
}

def lambda_handler(event, context):
    http_method = event.get('httpMethod', '')
    if http_method == 'OPTIONS':
        return {"statusCode": 200, "headers": CORS_HEADERS,
                "body": json.dumps({"message": "CORS preflight successful"})}

    try:
        path_params = event.get('pathParameters') or {}
        registration_id = path_params.get('id') or path_params.get('registrationId')

        if not registration_id:
            query_params = event.get('queryStringParameters') or {}
            registration_id = query_params.get('registrationId')

        if not registration_id and event.get('body'):
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
            registration_id = body.get('registrationId') or body.get('id')

        if not registration_id:
            return {"statusCode": 400, "headers": CORS_HEADERS,
                    "body": json.dumps({"error": "Registration ID required"})}

        response = db.table.scan(
            FilterExpression="registration_id = :rid",
            ExpressionAttributeValues={":rid": str(registration_id)}
        )
        items = response.get('Items', [])

        if not items:
            return {"statusCode": 404, "headers": CORS_HEADERS,
                    "body": json.dumps({"error": "Registration not found"})}

        for item in items:
            db.table.delete_item(Key={'PK': item['PK'], 'SK': item['SK']})

        return {"statusCode": 200, "headers": CORS_HEADERS,
                "body": json.dumps({"message": "Registration cancelled successfully"})}

    except ClientError as e:
        return {"statusCode": 500, "headers": CORS_HEADERS,
                "body": json.dumps({"error": "Failed to delete record from database", "details": str(e)})}
    except Exception as e:
        return {"statusCode": 500, "headers": CORS_HEADERS,
                "body": json.dumps({"error": "Internal server error", "details": str(e)})}
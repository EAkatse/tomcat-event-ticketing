<<<<<<< HEAD
from src.common.responses import success_response, error_response
from src.common.db import get_registrations_by_email
from src.common.validation import validate_email

def lambda_handler(event, context):
    try:
        # Get email from path parameters
        email = event.get('pathParameters', {}).get('email')
        
        # Validate email
        valid, message = validate_email(email)
        if not valid:
            return error_response(message, 400)
        
        # Get registrations
        items = get_registrations_by_email(email)
        
        registrations = []
        for item in items:
            registrations.append({
                'event_id': item.get('event_id'),
                'registration_id': item.get('registration_id'),
                'name': item.get('name'),
                'email': item.get('email'),
                'status': item.get('status', 'CONFIRMED')
            })
        
        return success_response({'registrations': registrations})
        
    except Exception as e:
        return error_response(str(e), 500)
=======
import json
import boto3
import os
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj) if obj % 1 != 0 else int(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'EventTicketingTable'))

def lambda_handler(event, context):
    try:
        email = event.get('pathParameters', {}).get('email')
        
        if not email:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': 'Email parameter required'})
            }
        
        response = table.query(
            IndexName='EmailIndex',
            KeyConditionExpression='GSI1PK = :email',
            ExpressionAttributeValues={':email': f'REG#{email}'}
        )
        
        registrations = []
        for item in response.get('Items', []):
            registrations.append({
                'event_id': item.get('event_id'),
                'registration_id': item.get('registration_id'),
                'name': item.get('name'),
                'email': item.get('email'),
                'status': item.get('status', 'CONFIRMED')
            })
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'registrations': registrations}, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }
>>>>>>> 4dff86f (Backend Code updates)

<<<<<<< HEAD
from src.common.responses import success_response, error_response
from src.common.db import table, decrement_registered_count

def lambda_handler(event, context):
    try:
        # Get registration ID from path parameters
        registration_id = event.get('pathParameters', {}).get('id')
        
        if not registration_id:
            return error_response('Registration ID required', 400)
        
        # Find the registration by scanning (simplified for demo)
        response = table.scan()
        found = False
        event_id = None
        email = None
        
        for item in response.get('Items', []):
            if item.get('registration_id') == registration_id:
                found = True
                event_id = item.get('event_id')
                email = item.get('email')
                break
        
        if not found:
            return error_response('Registration not found', 404)
        
        # Delete the registration
        table.delete_item(
            Key={'PK': f'EVENT#{event_id}', 'SK': f'REG#{email}'}
        )
        
        # Decrement registered count
        decrement_registered_count(event_id)
        
        return success_response({'message': 'Registration cancelled successfully'})
        
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
        registration_id = event.get('pathParameters', {}).get('id')
        
        if not registration_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': 'Registration ID required'})
            }
        
        response = table.scan()
        found = False
        event_id = None
        email = None
        
        for item in response.get('Items', []):
            if item.get('registration_id') == registration_id:
                found = True
                event_id = item.get('event_id')
                email = item.get('email')
                break
        
        if not found:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': 'Registration not found'})
            }
        
        table.delete_item(
            Key={'PK': f'EVENT#{event_id}', 'SK': f'REG#{email}'}
        )
        
        table.update_item(
            Key={'PK': f'EVENT#{event_id}', 'SK': 'METADATA'},
            UpdateExpression='ADD #r :dec',
            ExpressionAttributeNames={'#r': 'registered'},
            ExpressionAttributeValues={':dec': -1}
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Registration cancelled successfully'}, cls=DecimalEncoder)
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

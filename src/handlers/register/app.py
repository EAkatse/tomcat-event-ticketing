<<<<<<< HEAD
import json
import uuid
from datetime import datetime
from src.common.validation import validate_registration_input
from src.common.responses import success_response, error_response
from src.common.db import get_event, create_registration, increment_registered_count

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        event_id = body.get('event_id')
        email = body.get('email')
        name = body.get('name')
        
        # Validate input
        valid, message = validate_registration_input(event_id, email, name)
        if not valid:
            return error_response(message, 400)
        
        # Check if event exists
        event_item = get_event(event_id)
        if not event_item:
            return error_response('Event not found', 404)
        
        # Check capacity
        capacity = int(event_item.get('capacity', 0))
        registered = int(event_item.get('registered', 0))
        if registered >= capacity:
            return error_response('Event is full', 400)
        
        # Generate registration ID
        registration_id = str(uuid.uuid4())[:8]
        
        # Create registration
        create_registration(
            event_id=event_id,
            email=email,
            name=name,
            registration_id=registration_id,
            registered_at=datetime.now().isoformat()
        )
        
        # Increment registered count
        increment_registered_count(event_id)
        
        return success_response({
            'message': 'Registration confirmed',
            'registration_id': registration_id
        })
        
    except Exception as e:
        return error_response(str(e), 500)
=======
import json
import boto3
import os
import uuid
from datetime import datetime
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
        body = json.loads(event['body'])
        event_id = body.get('event_id')
        email = body.get('email')
        name = body.get('name')
        
        if not event_id or not email or not name:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': 'Missing required fields'})
            }
        
        # Check if event exists
        event_response = table.get_item(
            Key={'PK': f'EVENT#{event_id}', 'SK': 'METADATA'}
        )
        
        if 'Item' not in event_response:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': 'Event not found'})
            }
        
        event = event_response['Item']
        capacity = int(event.get('capacity', 0))
        registered = int(event.get('registered', 0))
        
        if registered >= capacity:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({'error': 'Event is full'})
            }
        
        registration_id = str(uuid.uuid4())[:8]
        
        table.put_item(
            Item={
                'PK': f'EVENT#{event_id}',
                'SK': f'REG#{email}',
                'GSI1PK': f'REG#{email}',
                'GSI1SK': f'EVENT#{event_id}',
                'registration_id': registration_id,
                'name': name,
                'email': email,
                'event_id': event_id,
                'registered_at': datetime.now().isoformat(),
                'status': 'CONFIRMED'
            }
        )
        
        table.update_item(
            Key={'PK': f'EVENT#{event_id}', 'SK': 'METADATA'},
            UpdateExpression='ADD #r :inc',
            ExpressionAttributeNames={'#r': 'registered'},
            ExpressionAttributeValues={':inc': 1}
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'message': 'Registration confirmed',
                'registration_id': registration_id
            }, cls=DecimalEncoder)
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
>>>>>>> 0068188 (Add SAM Event Registration API)

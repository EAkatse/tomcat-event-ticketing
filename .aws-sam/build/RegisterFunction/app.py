import json
import boto3
import os
import uuid
import time
import logging
from datetime import datetime
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj) if obj % 1 != 0 else int(obj)
        return super(DecimalEncoder, self).default(obj)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    start_time = time.time()
    
    try:
        logger.info(json.dumps({'event': event, 'timestamp': datetime.utcnow().isoformat() + 'Z'}))
        
        body = json.loads(event.get('body', '{}'))
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
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('TABLE_NAME', 'EventTicketingTable'))
        
        # Check event exists
        event_response = table.get_item(Key={'PK': f'EVENT#{event_id}', 'SK': 'METADATA'})
        
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
        
        event_item = event_response['Item']
        capacity = int(event_item.get('capacity', 0))
        registered = int(event_item.get('registered', 0))
        
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
        
        duration_ms = (time.time() - start_time) * 1000
        logger.info(json.dumps({'status': 200, 'duration_ms': duration_ms}))
        
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
            })
        }
        
    except Exception as e:
        logger.error(json.dumps({'error': str(e), 'timestamp': datetime.utcnow().isoformat() + 'Z'}))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }
import json
import boto3
import os
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
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.environ.get('TABLE_NAME', 'EventTicketingTable'))
        
        response = table.scan()
        events = []
        
        for item in response.get('Items', []):
            if item.get('SK') == 'METADATA':
                events.append({
                    'id': item.get('event_id'),
                    'name': item.get('name'),
                    'date': item.get('date'),
                    'capacity': int(item.get('capacity', 0)),
                    'registered': int(item.get('registered', 0))
                })
        
        duration_ms = (time.time() - start_time) * 1000
        logger.info(json.dumps({'status': 200, 'duration_ms': duration_ms}))
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'events': events}, cls=DecimalEncoder)
        }
        
    except Exception as e:
        logger.error(json.dumps({'error': str(e)}))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
        }
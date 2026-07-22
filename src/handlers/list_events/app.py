<<<<<<< HEAD
from src.common.responses import success_response, error_response
from src.common.db import table

def lambda_handler(event, context):
    try:
        # Scan for all events (items with SK='METADATA')
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
        
        return success_response({'events': events})
        
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

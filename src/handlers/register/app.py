import json
import uuid
from datetime import datetime
from common import db

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
}

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        event_id, email, name = body.get('event_id'), body.get('email'), body.get('name')

        if not event_id or not email or not name:
            return {'statusCode': 400, 'headers': CORS_HEADERS,
                    'body': json.dumps({'error': 'Missing required fields'})}

        event_item = db.table.get_item(Key={'PK': f'EVENT#{event_id}', 'SK': 'METADATA'}).get('Item')

        if not event_item:
            return {'statusCode': 404, 'headers': CORS_HEADERS,
                    'body': json.dumps({'error': 'Event not found'})}

        capacity = int(event_item.get('capacity', 0))
        registered = int(event_item.get('registered', 0))

        if registered >= capacity:
            return {'statusCode': 400, 'headers': CORS_HEADERS,
                    'body': json.dumps({'error': 'Event is full'})}

        registration_id = str(uuid.uuid4())[:8]

        db.table.put_item(Item={
            'PK': f'EVENT#{event_id}', 'SK': f'REG#{email}',
            'GSI1PK': f'REG#{email}', 'GSI1SK': f'EVENT#{event_id}',
            'registration_id': registration_id, 'name': name, 'email': email,
            'event_id': event_id, 'registered_at': datetime.now().isoformat(),
            'status': 'CONFIRMED'
        })

        db.table.update_item(
            Key={'PK': f'EVENT#{event_id}', 'SK': 'METADATA'},
            UpdateExpression='ADD #r :inc',
            ExpressionAttributeNames={'#r': 'registered'},
            ExpressionAttributeValues={':inc': 1}
        )

        return {'statusCode': 200, 'headers': CORS_HEADERS,
                'body': json.dumps({'message': 'Registration confirmed', 'registration_id': registration_id})}

    except Exception as e:
        return {'statusCode': 500, 'headers': CORS_HEADERS, 'body': json.dumps({'error': str(e)})}
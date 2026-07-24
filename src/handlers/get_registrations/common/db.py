import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'EventTicketingTable'))

def get_event(event_id):
    """Get an event by its ID."""
    response = table.get_item(
        Key={'PK': f'EVENT#{event_id}', 'SK': 'METADATA'}
    )
    return response.get('Item')

def create_registration(event_id, email, name, registration_id, registered_at):
    """Create a registration item in DynamoDB."""
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
            'registered_at': registered_at,
            'status': 'CONFIRMED'
        }
    )

def increment_registered_count(event_id):
    """Increment the registered count for an event."""
    table.update_item(
        Key={'PK': f'EVENT#{event_id}', 'SK': 'METADATA'},
        UpdateExpression='ADD #r :inc',
        ExpressionAttributeNames={'#r': 'registered'},
        ExpressionAttributeValues={':inc': 1}
    )

def decrement_registered_count(event_id):
    """Decrement the registered count for an event."""
    table.update_item(
        Key={'PK': f'EVENT#{event_id}', 'SK': 'METADATA'},
        UpdateExpression='ADD #r :dec',
        ExpressionAttributeNames={'#r': 'registered'},
        ExpressionAttributeValues={':dec': -1}
    )

def get_registrations_by_email(email):
    """Get all registrations for a given email using the GSI."""
    response = table.query(
        IndexName='EmailIndex',
        KeyConditionExpression='GSI1PK = :email',
        ExpressionAttributeValues={':email': f'REG#{email}'}
    )
    return response.get('Items', [])

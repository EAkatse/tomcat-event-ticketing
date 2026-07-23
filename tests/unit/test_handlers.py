import json
import pytest
from src.handlers.register import lambda_handler

def test_register_handler():
    event = {
        'body': json.dumps({
            'email': 'test@example.com',
            'event_id': 'EVT-001',
            'attendee_name': 'John Doe'
        })
    }
    response = lambda_handler(event, {})
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'registration_id' in body
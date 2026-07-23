import sys
import os
# This MUST point to cancel_registration, NOT register
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src', 'handlers', 'cancel_registration'))

import pytest
import json
from unittest.mock import patch, MagicMock
from app import lambda_handler

@pytest.fixture
def mock_table():
    with patch('common.db.table') as mock:
        yield mock

def test_cancel_success(mock_table):
    event = {
        'pathParameters': {
            'id': 'abc12345'
        }
    }
    
    mock_table.scan.return_value = {
        'Items': [
            {
                'registration_id': 'abc12345',
                'event_id': 'evt001',
                'email': 'test@email.com'
            }
        ]
    }
    
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['message'] == 'Registration cancelled successfully'

def test_cancel_not_found(mock_table):
    event = {
        'pathParameters': {
            'id': 'abc12345'
        }
    }
    
    mock_table.scan.return_value = {'Items': []}
    
    response = lambda_handler(event, None)
    assert response['statusCode'] == 404
    body = json.loads(response['body'])
    assert body['error'] == 'Registration not found'

def test_cancel_missing_id(mock_table):
    event = {'pathParameters': {}}
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert body['error'] == 'Registration ID required'
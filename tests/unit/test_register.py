import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src', 'handlers', 'register'))

import pytest
import json
from unittest.mock import patch, MagicMock
from app import lambda_handler

@pytest.fixture
def mock_table():
    with patch('common.db.table') as mock:
        yield mock

def test_register_success(mock_table):
    event = {
        'body': json.dumps({
            'event_id': 'evt001',
            'email': 'test@email.com',
            'name': 'Test User'
        })
    }
    
    mock_table.get_item.return_value = {
        'Item': {
            'capacity': 100,
            'registered': 50
        }
    }
    
    response = lambda_handler(event, None)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert 'registration_id' in body
    assert body['message'] == 'Registration confirmed'

def test_register_missing_fields(mock_table):
    event = {
        'body': json.dumps({
            'event_id': 'evt001'
        })
    }
    
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert 'error' in body

def test_register_event_not_found(mock_table):
    event = {
        'body': json.dumps({
            'event_id': 'evt001',
            'email': 'test@email.com',
            'name': 'Test User'
        })
    }
    
    mock_table.get_item.return_value = {}
    
    response = lambda_handler(event, None)
    assert response['statusCode'] == 404
    body = json.loads(response['body'])
    assert body['error'] == 'Event not found'

def test_register_event_full(mock_table):
    event = {
        'body': json.dumps({
            'event_id': 'evt001',
            'email': 'test@email.com',
            'name': 'Test User'
        })
    }
    
    mock_table.get_item.return_value = {
        'Item': {
            'capacity': 100,
            'registered': 100
        }
    }
    
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400
    body = json.loads(response['body'])
    assert body['error'] == 'Event is full'
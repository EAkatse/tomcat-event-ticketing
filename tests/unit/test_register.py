import sys
import os
import importlib.util

_handler_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src', 'handlers', 'register')
sys.path.insert(0, _handler_dir)

import pytest
import json
from unittest.mock import patch, MagicMock

_spec = importlib.util.spec_from_file_location("register_app", os.path.join(_handler_dir, "app.py"))
app = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(app)
lambda_handler = app.lambda_handler

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
import sys
import os
import importlib.util

_handler_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'src', 'handlers', 'cancel_registration')
sys.path.insert(0, _handler_dir)

import pytest
import json
from unittest.mock import patch, MagicMock

_spec = importlib.util.spec_from_file_location("cancel_app", os.path.join(_handler_dir, "app.py"))
app = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(app)
lambda_handler = app.lambda_handler

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
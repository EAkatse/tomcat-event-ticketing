import pytest
import json
import uuid
from datetime import datetime

@pytest.fixture
def sample_event():
    return {
        "PK": "EVENT#evt001",
        "SK": "METADATA",
        "event_id": "evt001",
        "name": "AWS Workshop Accra 2026",
        "date": "2026-08-15",
        "capacity": 100,
        "registered": 0
    }

@pytest.fixture
def sample_registration():
    return {
        "PK": "EVENT#evt001",
        "SK": "REG#test@email.com",
        "GSI1PK": "REG#test@email.com",
        "GSI1SK": "EVENT#evt001",
        "registration_id": str(uuid.uuid4())[:8],
        "name": "Test User",
        "email": "test@email.com",
        "event_id": "evt001",
        "registered_at": datetime.now().isoformat(),
        "status": "CONFIRMED"
    }

@pytest.fixture
def api_event_register():
    return {
        "body": json.dumps({
            "event_id": "evt001",
            "email": "test@email.com",
            "name": "Test User"
        })
    }

@pytest.fixture
def api_event_missing_fields():
    return {
        "body": json.dumps({
            "event_id": "evt001"
        })
    }

@pytest.fixture
def api_event_cancel():
    return {
        "pathParameters": {
            "id": "abc12345"
        }
    }
import json
import uuid
from datetime import datetime
from src.common.validation import validate_registration_input
from src.common.responses import success_response, error_response
from src.common.db import get_event, create_registration, increment_registered_count

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        event_id = body.get('event_id')
        email = body.get('email')
        name = body.get('name')
        
        # Validate input
        valid, message = validate_registration_input(event_id, email, name)
        if not valid:
            return error_response(message, 400)
        
        # Check if event exists
        event_item = get_event(event_id)
        if not event_item:
            return error_response('Event not found', 404)
        
        # Check capacity
        capacity = int(event_item.get('capacity', 0))
        registered = int(event_item.get('registered', 0))
        if registered >= capacity:
            return error_response('Event is full', 400)
        
        # Generate registration ID
        registration_id = str(uuid.uuid4())[:8]
        
        # Create registration
        create_registration(
            event_id=event_id,
            email=email,
            name=name,
            registration_id=registration_id,
            registered_at=datetime.now().isoformat()
        )
        
        # Increment registered count
        increment_registered_count(event_id)
        
        return success_response({
            'message': 'Registration confirmed',
            'registration_id': registration_id
        })
        
    except Exception as e:
        return error_response(str(e), 500)

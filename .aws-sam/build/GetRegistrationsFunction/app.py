from src.common.responses import success_response, error_response
from src.common.db import get_registrations_by_email
from src.common.validation import validate_email

def lambda_handler(event, context):
    try:
        # Get email from path parameters
        email = event.get('pathParameters', {}).get('email')
        
        # Validate email
        valid, message = validate_email(email)
        if not valid:
            return error_response(message, 400)
        
        # Get registrations
        items = get_registrations_by_email(email)
        
        registrations = []
        for item in items:
            registrations.append({
                'event_id': item.get('event_id'),
                'registration_id': item.get('registration_id'),
                'name': item.get('name'),
                'email': item.get('email'),
                'status': item.get('status', 'CONFIRMED')
            })
        
        return success_response({'registrations': registrations})
        
    except Exception as e:
        return error_response(str(e), 500)

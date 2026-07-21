from src.common.responses import success_response, error_response
from src.common.db import table, decrement_registered_count

def lambda_handler(event, context):
    try:
        # Get registration ID from path parameters
        registration_id = event.get('pathParameters', {}).get('id')
        
        if not registration_id:
            return error_response('Registration ID required', 400)
        
        # Find the registration by scanning (simplified for demo)
        response = table.scan()
        found = False
        event_id = None
        email = None
        
        for item in response.get('Items', []):
            if item.get('registration_id') == registration_id:
                found = True
                event_id = item.get('event_id')
                email = item.get('email')
                break
        
        if not found:
            return error_response('Registration not found', 404)
        
        # Delete the registration
        table.delete_item(
            Key={'PK': f'EVENT#{event_id}', 'SK': f'REG#{email}'}
        )
        
        # Decrement registered count
        decrement_registered_count(event_id)
        
        return success_response({'message': 'Registration cancelled successfully'})
        
    except Exception as e:
        return error_response(str(e), 500)

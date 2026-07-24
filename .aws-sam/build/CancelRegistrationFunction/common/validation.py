import re

def validate_email(email):
    """Validate email format."""
    if not email:
        return False, "Email is required"
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, ""

def validate_event_id(event_id):
    """Validate event_id format."""
    if not event_id:
        return False, "Event ID is required"
    if not isinstance(event_id, str) or len(event_id) < 3:
        return False, "Invalid event ID format"
    return True, ""

def validate_name(name):
    """Validate name is not empty."""
    if not name or not name.strip():
        return False, "Name is required"
    return True, ""

def validate_registration_input(event_id, email, name):
    """Validate all registration inputs."""
    errors = []
    
    valid, msg = validate_event_id(event_id)
    if not valid:
        errors.append(msg)
    
    valid, msg = validate_email(email)
    if not valid:
        errors.append(msg)
    
    valid, msg = validate_name(name)
    if not valid:
        errors.append(msg)
    
    if errors:
        return False, ", ".join(errors)
    return True, ""

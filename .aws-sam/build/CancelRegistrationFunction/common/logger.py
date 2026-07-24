import logging
import json
from datetime import datetime

def setup_logger():
    """Configure structured logging for Lambda functions."""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Remove default handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Add custom handler
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(handler)
    
    return logger

def log_event(logger, event, function_name):
    """Log the incoming event in JSON format."""
    logger.info(json.dumps({
        'function': function_name,
        'event': event,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }))

def log_error(logger, error, function_name, context=None):
    """Log an error in JSON format with context."""
    log_data = {
        'function': function_name,
        'error_type': type(error).__name__,
        'error_message': str(error),
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    if context:
        log_data['context'] = context
    logger.error(json.dumps(log_data))

def log_response(logger, function_name, status_code, duration=None):
    """Log the response in JSON format."""
    log_data = {
        'function': function_name,
        'status_code': status_code,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    if duration is not None:
        log_data['duration_ms'] = duration
    logger.info(json.dumps(log_data))
import json
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder for Decimal objects from DynamoDB."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj) if obj % 1 != 0 else int(obj)
        return super(DecimalEncoder, self).default(obj)

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
}

def success_response(data, status_code=200):
    """Return a successful API response with CORS headers."""
    return {
        'statusCode': status_code,
        'headers': CORS_HEADERS,
        'body': json.dumps(data, cls=DecimalEncoder)
    }

def error_response(message, status_code=400):
    """Return an error API response with CORS headers."""
    return {
        'statusCode': status_code,
        'headers': CORS_HEADERS,
        'body': json.dumps({'error': message})
    }

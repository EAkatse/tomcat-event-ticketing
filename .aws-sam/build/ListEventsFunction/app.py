from src.common.responses import success_response, error_response
from src.common.db import table

def lambda_handler(event, context):
    try:
        # Scan for all events (items with SK='METADATA')
        response = table.scan()
        events = []
        
        for item in response.get('Items', []):
            if item.get('SK') == 'METADATA':
                events.append({
                    'id': item.get('event_id'),
                    'name': item.get('name'),
                    'date': item.get('date'),
                    'capacity': int(item.get('capacity', 0)),
                    'registered': int(item.get('registered', 0))
                })
        
        return success_response({'events': events})
        
    except Exception as e:
        return error_response(str(e), 500)

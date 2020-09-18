def generate_db_response(event, context):
    if 'usercount' in event:
        response = {
            "user": event['user'],
            "state": "capacity"
        }

    else:
        response = {
            "user": event['user'],
            "state": event['state']
        }

    return response
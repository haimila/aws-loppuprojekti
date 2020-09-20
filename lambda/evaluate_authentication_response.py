def evaluate_authentication_response(event, context):
    if event['state'] == 'failed':
        response = {
            "access": "deny",
            "message": "Access denied. User authentication failed."
        }

    elif event['state'] == 'capacity':
        response = {
            "access": "deny",
            "message": "Access denied. Maximum number of concurrent users reached."
        }

    elif event['state'] == 'login':
        response = {
            "access": "allow",
            "message": "Access allowed. User logged in successfully."
        }

    elif event['state'] == 'logout':
        response = {
            "access": "allow",
            "message": "Access allowed. User logged out successfully."
        }

    else:
        response = "something unexpected happened"

    return {
        "user": event['user'],
        "response": response,
        "state": event['state']
    }
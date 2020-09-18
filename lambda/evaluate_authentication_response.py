def evaluate_authentication_response(event, context):
    if event['face'] == 'unknown':
        response = {
            "access": "deny",
            "message": "Access denied. Face recognition did not find a match."
        }

    elif event['face'] == 'notavailable':
        response = {
            "access": "deny",
            "message": "Access denied. Reference image for user not found."
        }

    elif event['state'] == 'capacity':
        response = {
            "access": "deny",
            "message": "Access denied. Maximum number of concurrent users reached."
        }

    elif event['state'] == 'login' and event['face'] == 'recognized':
        response = {
            "access": "allow",
            "message": "Access allowed. User logged in successfully."
        }

    elif event['state'] == 'logout' and event['face'] == 'recognized':
        response = {
            "access": "allow",
            "message": "Access allowed. User logged out successfully."
        }

    else:
        response = "something unexpected happened"

    return {
        "user": event['user'],
        "response": response
    }
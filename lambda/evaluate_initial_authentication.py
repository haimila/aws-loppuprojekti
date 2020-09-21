def evaluate_initial_authentication(event, context):
    if event[0]['user']['id'] == 'unknown' or event[1]['face'] == 'notavailable' or event[1]['face'] == 'unknown':
        response = {
            "user": event[0]["user"],
            "state": "failed"
        }
    else:
        response = {
            "user": event[0]["user"],
            "state": "continue"
        }
    return response


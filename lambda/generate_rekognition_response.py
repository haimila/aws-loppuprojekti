
def generate_rekognition_response(event, context):
    return {"face": event['face']}
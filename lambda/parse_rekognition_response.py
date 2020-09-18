def parse_rekognition_response(event, context):

    if len(event['face']['FaceMatches']) > 0:
        return {"face": "recognized"}
    else:
        return {"face": "unknown"}
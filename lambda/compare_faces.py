import boto3

client = boto3.client('rekognition', region_name='us-east-1')


def compare_faces(event, contex):
    try:
        userid = event['userid']
        sourceimage = f'{userid}.jpg'
        targetimage = f'{userid}-capture.jpg'

        facedata = client.compare_faces(
            SimilarityThreshold=90,
            SourceImage={
                'S3Object': {
                    'Bucket': 'rasberry-bucket',
                    'Name': sourceimage
                }
            },
            TargetImage={
                'S3Object': {
                    'Bucket': 'rasberry-bucket',
                    'Name': targetimage
                }
            }
        )

        response = {"face": facedata}

    except:
        response = {"face": "notavailable"}

    finally:
        return response
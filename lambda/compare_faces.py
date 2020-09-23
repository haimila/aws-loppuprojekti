import boto3
import os

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
                    'Bucket': os.environ['original_photo_bucket'],
                    'Name': sourceimage
                }
            },
            TargetImage={
                'S3Object': {
                    'Bucket': os.environ['capture_photo_bucket'],
                    'Name': targetimage
                }
            }
        )

        response = {"face": facedata}

    except:
        response = {"face": "notavailable"}

    finally:
        return response
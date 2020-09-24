import boto3
import os

s3 = boto3.resource('s3')
bucket = s3.Bucket(os.environ['original_photo_bucket'])


def stream_delete_event_to_s3(event, context):
    try:
        userid = event['Records'][0]['dynamodb']['Keys']['id']['S']

        if event['Records'][0]['eventName'] == 'REMOVE':

            bucket.delete_objects(
                Delete={
                    'Objects': [
                        {
                            'Key': f'{userid}.jpg'
                        }]})

        else:
            pass

    except:
        pass

    return {"message": f"user {userid} deleted"}
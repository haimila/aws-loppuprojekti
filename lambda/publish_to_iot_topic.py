import boto3
import json

client = boto3.client('iot-data', region_name='us-east-1')


def publish_to_iot(event, context):
    client.publish(
        topic='raspberry/accesstopic',
        payload=json.dumps(event)
    )
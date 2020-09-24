import boto3
import json
import os

client = boto3.client('iot-data', region_name=os.environ['region'])


def publish_to_iot(event, context):
    client.publish(
        topic='raspberry/accesstopic',
        payload=json.dumps(event)
    )
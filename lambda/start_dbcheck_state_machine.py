import json
import boto3
import os

sfn = boto3.client('stepfunctions', region_name=os.environ['region'])

def start_state_machine(event, context):

    objectkey = event['Records'][0]['s3']['object']['key']
    userid = objectkey[:-12]

    sfn.start_execution(
        stateMachineArn=os.environ['state_machine'],
        input=json.dumps({"userid": userid}))
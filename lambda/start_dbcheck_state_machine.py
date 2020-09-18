import json
import boto3

sfn = boto3.client('stepfunctions', region_name='us-east-1')

def start_state_machine(event, context):

    objectkey = event['Records'][0]['s3']['object']['key']
    userid = objectkey[:-12]

    sfn.start_execution(
        stateMachineArn='arn:aws:states:us-east-1:821383200340:stateMachine:AccessControlDBCheck',
        input=json.dumps({"userid": userid}))
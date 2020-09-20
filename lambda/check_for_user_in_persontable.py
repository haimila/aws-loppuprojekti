import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('person')

def get_user(event, context):
    try:
        userid = event['userid']
        resp = table.get_item(Key={"id": event['userid']})
        userdata = resp['Item']
        response = {
            "user": userdata
        }
    except:
        response = {
            "user": "unknown"
        }
    return response
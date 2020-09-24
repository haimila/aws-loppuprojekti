import os
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(os.environ['active_table'])


def check_if_user_is_active(event, context):
    try:
        userid = event['user']['id']
        resp = table.get_item(Key={"id": userid})
        userdata = resp['Item']
        response = {
            "user": userdata,
            "logout": "true"
        }
    except:
        response = {
            "user": event['user'],
            "login": "true"
        }
    return response
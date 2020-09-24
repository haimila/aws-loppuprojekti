import os
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(os.environ['active_table'])


def remove_user_from_active_table(event, context):
    userid = event['user']['id']
    table.delete_item(Key={'id': userid})

    return {
        "user": event['user'],
        "state": "logout"
    }
import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('active')


def remove_user_from_active_table(event, context):
    userid = event['user']['id']
    table.delete_item(Key={'id': userid})

    return {
        "message": "User logged out succesfully"
    }

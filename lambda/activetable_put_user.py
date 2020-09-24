import json
import boto3
import os

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(os.environ['active_table'])


def create_active_user(event, context):
    userdata = event['user']

    item = {
        'id': userdata['id'],
        'firstname': userdata['firstname'],
        'lastname': userdata['lastname']
    }
    table.put_item(Item=item)

    return {"user": event['user']}


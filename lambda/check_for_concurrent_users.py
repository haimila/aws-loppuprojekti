import json
import boto3

dynamodb = boto3.client('dynamodb', region_name='us-east-1')


def check_for_concurrent_users(event, context):
    checklist = []
    userlist = dynamodb.scan(TableName='active')

    users = userlist['Items']

    for user in users:
        checklist.append(user['id'])

    usercount = len(checklist)
    print(type(usercount))
    response = {
        "user": event['user'],
        "usercount": len(checklist)
    }

    return response
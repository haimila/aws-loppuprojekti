import os
import boto3

dynamodb = boto3.client('dynamodb', region_name=os.environ['region'])

# scans the Active table for user ids and produces a list with a length equal to the number of userids in the table

def check_for_concurrent_users(event, context):
    checklist = []
    userlist = dynamodb.scan(TableName=os.environ['active_table'])

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
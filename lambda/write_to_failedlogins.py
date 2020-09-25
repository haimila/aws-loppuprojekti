import boto3
from datetime import datetime
import uuid
import os

dynamodb = boto3.resource('dynamodb', region_name=os.environ['region'])
table = dynamodb.Table(os.environ['failedlogins_table'])


def write_to_failed_login_table(event, context):
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")

    if event['user'] == 'unknown':
        item = {
            'eventid': str(uuid.uuid4()),
            'userid': event['user'],
            'timestamp': timestampStr,
            'message': event['response']['message']
        }
    else:
        item = {
            'eventid': str(uuid.uuid4()),
            'userid': event['user']['id'],
            'timestamp': timestampStr,
            'message': event['response']['message']
        }

    table.put_item(Item=item)

    response = event['response']

    return response
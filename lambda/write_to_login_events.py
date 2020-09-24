import boto3
from datetime import datetime
import uuid
import os

dynamodb = boto3.resource('dynamodb', region_name=os.environ['region'])
table = dynamodb.Table(os.environ['loginevents_table'])


def write_to_login_events(event, context):
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")

    item = {
        'eventid': str(uuid.uuid4()),
        'userid': event['user']['id'],
        'timestamp': timestampStr
    }
    table.put_item(Item=item)

    response = event['response']

    return response
import boto3
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('failedlogins')


def write_to_failed_login_table(event, context):
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")

    item = {
        'eventid': str(uuid.uuid4()),
        'userid': event['user']['id'],
        'timestamp': timestampStr,
        'message': event['response']['message']
    }
    table.put_item(Item=item)

    response = event['response']

    return response
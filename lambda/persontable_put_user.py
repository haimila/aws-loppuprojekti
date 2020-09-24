import json
import boto3
import os

dynamodb = boto3.resource('dynamodb', region_name=os.environ['region'])
table = dynamodb.Table(os.environ['person_table'])


def create_new_user(event, context):
    message = event['Records'][0]['Sns']['Message']
    userdata = json.loads(message)

    item = {
        'id': userdata['userId'],
        'firstname': userdata['firstName'],
        'lastname': userdata['lastName']
    }
    table.put_item(Item=item)

    return {
        "created": json.dumps(item)
    }




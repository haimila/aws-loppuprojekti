
import boto3
import os

dynamodb = boto3.resource('dynamodb', region_name=os.environ['region'])
table = dynamodb.Table(os.environ['active_table'])

# adds user to Active table. Returns "login" state for further state machine functionality
def create_active_user(event, context):
    userdata = event['user']

    item = {
        'id': userdata['id'],
        'firstname': userdata['firstname'],
        'lastname': userdata['lastname']
    }
    table.put_item(Item=item)

    return {"user": event['user'],
            "state": "login"
            }


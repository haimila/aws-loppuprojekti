import boto3

client = boto3.client('ssm', region_name='us-east-1')

def codepipeline_to_raspberry(event, context):
    client.send_command(
        Targets=[
            {
                'Key': 'InstanceIds',
                'Values': [
                    'mi-03202040d3b3c0bc4'
                ]
            },
        ],
        DocumentName='AWS-RunShellScript',
        Parameters={"commands": ["sudo git pull"],
                    "workingDirectory": ["/home/pi/AccessProject/"]
                    })


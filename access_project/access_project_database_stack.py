from aws_cdk import (
    aws_s3 as s3,
    aws_dynamodb as dynamodb,
    core
)
class DatabaseStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create a bucket "vattubuck"
        bucket = s3.Bucket(
            self,"vattubuck",
            versioned=True, )

        # create a table called "person"
        self._table = dynamodb.Table(
            self, 'person',
            partition_key={'name': 'id', 'type': dynamodb.AttributeType.STRING},
        )

        # create a table called "active"
        self._table = dynamodb.Table(
            self, 'active',
            partition_key={'name': 'id', 'type': dynamodb.AttributeType.STRING},
        )

        # create a table called "loginevents"
        self._table = dynamodb.Table(
            self, 'loginevents',
            partition_key={'name': 'eventid', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'userid', 'type': dynamodb.AttributeType.STRING}
        )

        # create a table called "logoutevents"
        self._table = dynamodb.Table(
            self, 'logoutevents',
            partition_key={'name': 'eventid', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'userid', 'type': dynamodb.AttributeType.STRING}
        )

        # create a table called "failedlogins"
        self._table = dynamodb.Table(
            self, 'failedlogins',
            partition_key={'name': 'eventid', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'userid', 'type': dynamodb.AttributeType.STRING}
        )
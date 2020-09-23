from aws_cdk import (
    aws_dynamodb as dynamodb,
    core
)
class DatabaseStack(core.Stack):

    @property
    def person_table(self, _default=None):
        return self._person_table

    @property
    def active_table(self, _default=None):
        return self._active_table

    @property
    def loginevents_table(self, _default=None):
        return self._loginevents_table

    @property
    def logoutevents_table(self, _default=None):
        return self._logoutevents_table

    @property
    def failedlogins_table(self, _default=None):
        return self._failedlogins_table

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create a table called "person"
        self._person_table = dynamodb.Table(
            self, 'person',
            partition_key={'name': 'id', 'type': dynamodb.AttributeType.STRING},
        )

        # create a table called "active"
        self._active_table = dynamodb.Table(
            self, 'active',
            partition_key={'name': 'id', 'type': dynamodb.AttributeType.STRING},
        )

        # create a table called "loginevents"
        self._loginevents_table = dynamodb.Table(
            self, 'loginevents',
            partition_key={'name': 'eventid', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'userid', 'type': dynamodb.AttributeType.STRING}
        )

        # create a table called "logoutevents"
        self._logoutevents_table = dynamodb.Table(
            self, 'logoutevents',
            partition_key={'name': 'eventid', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'userid', 'type': dynamodb.AttributeType.STRING}
        )

        # create a table called "failedlogins"
        self._failedlogins_table = dynamodb.Table(
            self, 'failedlogins',
            partition_key={'name': 'eventid', 'type': dynamodb.AttributeType.STRING},
            sort_key={'name': 'userid', 'type': dynamodb.AttributeType.STRING}
        )
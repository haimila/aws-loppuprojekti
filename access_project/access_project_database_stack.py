from aws_cdk import (
    aws_dynamodb as dynamodb,
    core, aws_dynamodb
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
            partition_key=aws_dynamodb.Attribute(
                name='id',
                type=aws_dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1
        )

        # create a table called "active"
        self._active_table = dynamodb.Table(
            self, 'active',
            partition_key=aws_dynamodb.Attribute(
                name='id',
                type=aws_dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1
        )

        # create a table called "loginevents"
        self._loginevents_table = dynamodb.Table(
            self, 'loginevents',
            partition_key=aws_dynamodb.Attribute(
                name='eventid',
                type=aws_dynamodb.AttributeType.STRING),
            sort_key=aws_dynamodb.Attribute(
                name='userid',
                type=aws_dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1
            )

        self._loginevents_table.add_global_secondary_index(
            index_name='userid-timestamp-index',
            partition_key=aws_dynamodb.Attribute(
                name='userid',
                type=aws_dynamodb.AttributeType.STRING),
            sort_key=aws_dynamodb.Attribute(
                name='timestamp',
                type=aws_dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1
        )

        # create a table called "logoutevents"
        self._logoutevents_table = dynamodb.Table(
            self, 'logoutevents',
            partition_key=aws_dynamodb.Attribute(
                name='eventid',
                type=aws_dynamodb.AttributeType.STRING),
            sort_key=aws_dynamodb.Attribute(
                name='userid',
                type=aws_dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1
        )

        self._logoutevents_table.add_global_secondary_index(
            index_name='userid-timestamp-index',
            partition_key=aws_dynamodb.Attribute(
                name='userid',
                type=aws_dynamodb.AttributeType.STRING),
            sort_key=aws_dynamodb.Attribute(
                name='timestamp',
                type=aws_dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1
        )

        # create a table called "failedlogins"
        self._failedlogins_table = dynamodb.Table(
            self, 'failedlogins',
            partition_key=aws_dynamodb.Attribute(
                name='eventid',
                type=aws_dynamodb.AttributeType.STRING),
            sort_key=aws_dynamodb.Attribute(
                name='userid',
                type=aws_dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1
        )

        self._failedlogins_table.add_global_secondary_index(
            index_name='userid-timestamp-index',
            partition_key=aws_dynamodb.Attribute(
                name='userid',
                type=aws_dynamodb.AttributeType.STRING),
            sort_key=aws_dynamodb.Attribute(
                name='timestamp',
                type=aws_dynamodb.AttributeType.STRING),
            read_capacity=1,
            write_capacity=1
        )

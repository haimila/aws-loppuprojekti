from aws_cdk import (
    aws_s3 as s3,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    core
)

class AccessProjectStack(core.Stack):

    @property
    def bucket(self, _default = None):
        return self._bucket

    def __init__(self, scope: core.Construct, id: str, active_table: dynamodb.Table, person_table: dynamodb.Table, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create a bucket "AccessProjectBucket"
        self._bucket = s3.Bucket(
            self, "AccessProjectBucket",
            versioned=True
        )

        # create a bucket "AccessProjectCaptureBucket"
        self._capture_bucket = s3.Bucket(
            self, "AccessProjectCaptureBucket"
        )

        self._capture_bucket = s3.LifecycleRule(
            expiration=1
        )

        # create a topic "WriteTag"
        write_topic = sns.Topic(
            self, "WriteTag"
        )

        # create a topic "SendUserDataToRaspberryPi"
        send_topic = sns.Topic(
            self, "SendUserDataToRaspberryPi"
        )

        # create an iam policy statement to allow lambda function to write to dynamodb active table
        write_to_activetable_policy_statement = iam.PolicyStatement(
            actions=["dynamodb:PutItem"],
            resources=[active_table.table_arn]
        )

        # create a lambda function "create_active_user"
        activetable_put_user = _lambda.Function(
            self, 'ActivetablePutUserHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='activetable_put_user.create_active_user',
            initial_policy=[write_to_activetable_policy_statement]
        )

        # create a lambda subscription for "WriteTag" topic
        write_topic.add_subscription(subscriptions.LambdaSubscription(activetable_put_user))

        # create an iam policy statement to allow lambda function to remove user from dynamodb active table
        delete_user_from_activetable_policy_statement = iam.PolicyStatement(
            actions=["dynamodb:DeleteItem"],
            resources=[active_table.table_arn]
        )

        # create a lambda function "remove_user_from_active_table"
        activetable_remove_user = _lambda.Function(
            self, 'ActivetableRemoveUserHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='activetable_remove_user.remove_user_from_active_table',
            initial_policy=[delete_user_from_activetable_policy_statement]
        )

        # create an iam policy statement to allow lambda function to check for concurrent users from active table
        check_for_concurrent_users_policy_statement = iam.PolicyStatement(
            actions=["dynamodb:Scan"],
            resources=[active_table.table_arn]
        )

        # create a lambda function "check_for_concurrent_users"
        check_for_concurrent_users = _lambda.Function(
            self, 'CheckForConcurrentUsersHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='check_for_concurrent_users.check_for_concurrent_users',
            initial_policy=[check_for_concurrent_users_policy_statement]
        )

        # create an iam policy statement to allow lambda function to check if person exists in person table
        check_for_user_in_persontable_policy_statement = iam.PolicyStatement(
            actions=["dynamodb:GetItem"],
            resources=[person_table.table_arn]
        )

        # create a lambda function "get_user"
        check_for_user_in_persontable = _lambda.Function(
            self, 'CheckForUserInPersontableHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='check_for_user_in_persontable.get_user',
            initial_policy=[check_for_user_in_persontable_policy_statement]
        )

        # create an iam policy statement to allow lambda function to check if user exists in active table
        check_if_user_is_active_policy_statement = iam.PolicyStatement(
            actions=["dynamodb:GetItem"],
            resources=[active_table.table_arn]
        )

        # create a lambda function "check_if_user_is_active"
        check_if_user_is_active = _lambda.Function(
            self, 'CheckIfUserIsActiveHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='check_if_user_is_active.check_if_user_is_active',
            initial_policy=[check_if_user_is_active_policy_statement]
        )

        # create an iam policy statement to allow lambda function to get object from access project bucket
        compare_faces_bucket_policy_statement = iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[self._bucket.bucket_arn]
        )

        # create an iam policy statement to allow lambda function to use rekognition
        rekognition_policy_statement = iam.PolicyStatement(
            actions=["rekognition:CompareFaces"],
            resources=["*"]
        )

        # create a lambda function "compare_faces"
        compare_faces = _lambda.Function(
            self, 'CompareFacesHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='compare_faces.compare_faces',
            initial_policy=[compare_faces_bucket_policy_statement, rekognition_policy_statement]
        )

        # create a lambda function "evaluate_authentication_response"
        evaluate_authentication_response = _lambda.Function(
            self, 'EvaluateAuthenticationResponseHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='evaluate_authentication_response.evaluate_authentication_response',
            role=iam.Role.from_role_arn(self, "Role6", "arn:aws:iam::821383200340:role/service-role/EvaluateAuthenticationResponse-role-n1k99vpx"),
        )

        # create a lambda function "evaluate_initial_authentication"
        evaluate_initial_authentication = _lambda.Function(
            self, 'EvaluateInitialAuthenticationHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='evaluate_initial_authentication.evaluate_initial_authentication',
            role=iam.Role.from_role_arn(self, "Role7", "arn:aws:iam::821383200340:role/service-role/EvaluateInitialAuthentication-role-a3tjga8s"),
        )

        # create a lambda function "generate_db_response"
        generate_db_response = _lambda.Function(
            self, 'GenerateDbResponseHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='generate_db_response.generate_db_response',
            role=iam.Role.from_role_arn(self, "Role8", "arn:aws:iam::821383200340:role/service-role/EvaluateInitialAuthentication-role-a3tjga8s"),
        )

        # create a lambda function "parse_rekognition_response"
        parse_rekognition_response = _lambda.Function(
            self, 'ParseRekognitionResponseHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='parse_rekognition_response.parse_rekognition_response',
            role=iam.Role.from_role_arn(self, "Role9", "arn:aws:iam::821383200340:role/service-role/ParseRekognitionResponse-role-c8tpa6ie"),
        )

        # create an iam policy statement to allow lambda function to create user to person table
        person_table_put_user_policy_statement = iam.PolicyStatement(
            actions=["dynamodb:PutItem"],
            resources=[person_table.table_arn]
        )

        # create a lambda function "create_new_user"
        persontable_put_user = _lambda.Function(
            self, 'PersontablePutUserHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='persontable_put_user.create_new_user',
            initial_policy=[person_table_put_user_policy_statement]
        )

        # create a lambda function "send_notification_response"
        publish_to_iot_topic = _lambda.Function(
            self, 'PublishToIoTTopicHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='publish_to_iot_topic.publish_to_iot'
        )

        # create a lambda function "start_state_machine"
        start_state_machine = _lambda.Function(
            self, 'StartStateMachineHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='start_state-machine.start_state_machine',
            role=iam.Role.from_role_arn(self, "Role12", "arn:aws:iam::821383200340:role/service-role/StartStateMachine-role-a84dxv22"),
        )

        # create a lambda function "write_to_failed_login_table"
        write_to_failedlogins = _lambda.Function(
            self, 'WriteToFailedloginsHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='write_to_failedlogins.write_to_failed_login_table',
            role=iam.Role.from_role_arn(self, "Role13", "arn:aws:iam::821383200340:role/service-role/WriteToFailedLoginTable-role-n6284xpn"),
        )

        # create a lambda function "write_to_login_events"
        write_to_login_events = _lambda.Function(
            self, 'WriteToLoginEventsHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='write_to_login_events.write_to_login_events',
            role=iam.Role.from_role_arn(self, "Role14", "arn:aws:iam::821383200340:role/service-role/WriteToLoginEvents-role-mq6s2b7w"),
        )

        # create a lambda function "write_to_logout_events"
        write_to_logout_events = _lambda.Function(
            self, 'WriteToLogoutEventsHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='write_to_logout_events.write_to_logout_events',
            role=iam.Role.from_role_arn(self, "Role15", "arn:aws:iam::821383200340:role/service-role/WriteToLogoutEvents-role-efapsztj"),
        )
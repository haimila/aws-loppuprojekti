from aws_cdk import (
    aws_s3 as s3,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_lambda as _lambda,
    core
)

class AccessProjectStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create a bucket "vattubuck"
        bucket = s3.Bucket(
            self, "vattubuck",
            versioned=True, )

        # create a topic "WriteTag"
        write_topic = sns.Topic(
            self, "WriteTag"
        )

        # create a topic "SendUserDataToRaspberryPi"
        send_topic = sns.Topic(
            self, "SendUserDataToRaspberryPi"
        )

        # create a lambda function "create_active_user"
        activetable_put_user = _lambda.Function(
            self, 'ActivetablePutUserHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='activetable_put_user.create_active_user',
        )

        # create a lambda subscription for "WriteTag" topic
        write_topic.add_subscription(subscriptions.LambdaSubscription(activetable_put_user))

        # create a lambda function "remove_user_from_active_table"
        activetable_remove_user = _lambda.Function(
            self, 'ActivetableRemoveUserHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='activetable_remove_user.remove_user_from_active_table',
        )

        # create a lambda function "check_for_concurrent_users"
        check_for_concurrent_users = _lambda.Function(
            self, 'CheckForConcurrentUsersHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='check_for_concurrent_users.check_for_concurrent_users',
        )

        # create a lambda function "get_user"
        check_for_user_in_persontable = _lambda.Function(
            self, 'CheckForUserInPersontableHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='check_for_user_in_persontable.get_user',
        )

        # create a lambda function "check_if_user_is_active"
        check_if_user_is_active = _lambda.Function(
            self, 'CheckIfUserIsActiveHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='check_if_user_is_active.check_if_user_is_active',
        )

        # create a lambda function "compare_faces"
        compare_faces = _lambda.Function(
            self, 'CompareFacesHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='compare_faces.compare_faces',
        )

        # create a lambda function "evaluate_authentication_response"
        evaluate_authentication_response = _lambda.Function(
            self, 'EvaluateAuthenticationResponseHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='evaluate_authentication_response.evaluate_authentication_response'
        )

        # create a lambda function "evaluate_initial_authentication"
        evaluate_initial_authentication = _lambda.Function(
            self, 'EvaluateInitialAuthenticationHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='evaluate_initial_authentication.evaluate_initial_authentication'
        )

        # create a lambda function "generate_db_response"
        generate_db_response = _lambda.Function(
            self, 'GenerateDbResponseHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='generate_db_response.generate_db_response',
        )

        # create a lambda function "parse_rekognition_response"
        parse_rekognition_response = _lambda.Function(
            self, 'ParseRekognitionResponseHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='parse_rekognition_response.parse_rekognition_response',
        )

        # create a lambda function "create_new_user"
        persontable_put_user = _lambda.Function(
            self, 'PersontablePutUserHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='persontable_put_user.create_new_user',
        )

        # create a lambda function "send_notification_response"
        send_notification_response = _lambda.Function(
            self, 'SendNotificationResponseHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='send_notification_response.send_notification_response',
        )

        # create a lambda function "start_state_machine"
        start_dbcheck_state_machine = _lambda.Function(
            self, 'StartDbcheckStateMachineHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='start_dbcheck_state-machine.start_state_machine',
        )

        # create a lambda function "write_to_failed_login_table"
        write_to_failedlogins = _lambda.Function(
            self, 'WriteToFailedloginsHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='write_to_failedlogins.write_to_failed_login_table',
        )

        # create a lambda function "write_to_login_events"
        write_to_login_events = _lambda.Function(
            self, 'WriteToLoginEventsHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='write_to_login_events.write_to_login_events',
        )

        # create a lambda function "write_to_logout_events"
        write_to_logout_events = _lambda.Function(
            self, 'WriteToLogoutEventsHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='write_to_logout_events.write_to_logout_events',
        )
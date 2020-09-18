from aws_cdk import (
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_lambda as _lambda,
    core
)

class AccessProjectStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        write_topic = sns.Topic(
            self, "WriteTag"
        )

        send_topic = sns.Topic(
            self, "SendUserDataToRaspberryPi"
        )

        # Defines an AWS Lambda resource
        activetable_put_user = _lambda.Function(
            self, 'ActivetablePutUserHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='activetable_put_user.create_active_user',
        )

        write_topic.add_subscription(subscriptions.LambdaSubscription(activetable_put_user))

        persontable_put_user = _lambda.Function(
            self, 'PersontablePutUserHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='persontable_put_user.create_new_user',
        )

        activetable_remove_user = _lambda.Function(
            self, 'ActivetableRemoveUserHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='activetable_remove_user.remove_user_from_active_table',
        )

        check_for_concurrent_users = _lambda.Function(
            self, 'CheckForConcurrentUsersHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='check_for_concurrent_users.check_for_concurrent_users',
        )

        check_for_user_in_persontable = _lambda.Function(
            self, 'CheckForUserInPersontableHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='check_for_user_in_persontable.get_user',
        )

        check_if_user_is_active = _lambda.Function(
            self, 'CheckIfUserIsActiveHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='check_if_user_is_active.check_if_user_is_active',
        )

        compare_faces = _lambda.Function(
            self, 'CompareFacesHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='compare_faces.compare_faces',
        )

        evaluate_authentication_response = _lambda.Function(
            self, 'EvaluateAuthenticationResponseHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='evaluate_authentication_response.evaluate_authentication_response',
        )

        parse_rekognition_response = _lambda.Function(
            self, 'ParseRekognitionResponseHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='parse_rekognition_response.parse_rekognition_response',
        )

        generate_db_response = _lambda.Function(
            self, 'GenerateDbResponseHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='generate_db_response.generate_db_response',
        )

        start_dbcheck_state_machine = _lambda.Function(
            self, 'StartDbcheckStateMachineHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='start_dbcheck_state-machine.start_state_machine',
        )
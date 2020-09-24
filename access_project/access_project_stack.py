from aws_cdk import (
    aws_s3 as s3,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_stepfunctions as sf,
    aws_s3_notifications as notifications,
    core
)

class AccessProjectStack(core.Stack):

    @property
    def bucket(self, _default = None):
        return self._bucket

    @property
    def capture_bucket(self, _default=None):
        return self._capture_bucket

    @property
    def write_topic(self, _default=None):
        return self._write_topic

    def __init__(self, scope: core.Construct, id: str,
                 active_table: dynamodb.Table,
                 person_table: dynamodb.Table, failedlogins_table: dynamodb.Table,
                 loginevents_table: dynamodb.Table, logoutevents_table: dynamodb.Table,
                 **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create a bucket "AccessProjectBucket"
        self._bucket = s3.Bucket(
            self, "AccessProjectBucket",
            versioned=True
        )

        # create a lifecycle rule for "AccessProjectCaptureBucket" to remove object after one day from creation
        lifecycle_rule = s3.LifecycleRule(
            expiration=core.Duration.days(1)
        )

        # create a bucket "AccessProjectCaptureBucket"
        self._capture_bucket = s3.Bucket(
            self, "AccessProjectCaptureBucket",
            lifecycle_rules=[lifecycle_rule]
            )

        # create a topic "WriteTag"
        self._write_topic = sns.Topic(
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
            initial_policy=[write_to_activetable_policy_statement],
            environment={"active_table": active_table.table_name}
        )

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
            initial_policy=[delete_user_from_activetable_policy_statement],
            environment={"active_table": active_table.table_name}
        )

        #create an iam policy statement to allow lambda function to check for concurrent users from active table
        check_for_concurrent_users_policy_statement = iam.PolicyStatement(
            actions=["dynamodb:Scan"],
            resources=[active_table.table_arn],

        )

        # create a lambda function "check_for_concurrent_users"
        check_for_concurrent_users = _lambda.Function(
            self, 'CheckForConcurrentUsersHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='check_for_concurrent_users.check_for_concurrent_users',
            initial_policy=[check_for_concurrent_users_policy_statement],
            environment={"active_table": active_table.table_name}
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
            initial_policy=[check_for_user_in_persontable_policy_statement],
            environment={"person_table": person_table.table_name}
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
            initial_policy=[check_if_user_is_active_policy_statement],
            environment={"active_table": active_table.table_name}
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
            initial_policy=[compare_faces_bucket_policy_statement, rekognition_policy_statement],
            environment={"original_photo_bucket": self._bucket.bucket_name,
                         "capture_photo_bucket": self._capture_bucket.bucket_name
                         }
        )

        # create a lambda function "generate_rekognition_response"
        generate_rekognition_response = _lambda.Function(
            self, 'GenerateRekognitionResponse',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='generate_rekognition_response.generate_rekognition_response'
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
            handler='generate_db_response.generate_db_response'
        )

        # create a lambda function "parse_rekognition_response"
        parse_rekognition_response = _lambda.Function(
            self, 'ParseRekognitionResponseHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='parse_rekognition_response.parse_rekognition_response'
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
            initial_policy=[person_table_put_user_policy_statement],
            environment={"person_table": person_table.table_name}
        )

        # create a lambda subscription for "WriteTag" topic
        self._write_topic.add_subscription(subscriptions.LambdaSubscription(persontable_put_user))

        # create an iam policy statement to allow lambda function to publish to iot topic
        publish_to_iot_policy_statement = iam.PolicyStatement(
            actions=["iot:Publish"],
            resources=["*"]
        )

        # create a lambda function "publish_to_iot"
        publish_to_iot_topic = _lambda.Function(
            self, 'PublishToIoTTopicHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='publish_to_iot_topic.publish_to_iot',
            initial_policy=[publish_to_iot_policy_statement]
        )

        # create a lamdba function "stream_delete_event_to_s3"
        stream_delete_event_to_s3 = _lambda.Function(
            self, 'StreamDeleteEventToS3',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='stream_delete_event_to_s3.stream_delete_event_to_s3',
            environment={"original_photo_bucket": self._bucket.bucket_name}
        )

        # create an iam policy statement to allow lambda function to write to failedloginevents table
        write_to_failed_login_table_policy_statement = iam.PolicyStatement(
            actions=["dynamodb:PutItem"],
            resources=[failedlogins_table.table_arn]
        )

        # create a lambda function "write_to_failed_login_table"
        write_to_failedlogins = _lambda.Function(
            self, 'WriteToFailedloginsHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='write_to_failedlogins.write_to_failed_login_table',
            initial_policy=[write_to_failed_login_table_policy_statement],
            environment={"failedlogins_table": failedlogins_table.table_arn}
        )

        # create an iam policy statement to allow lambda function to write to loginevents table
        write_to_login_events_policy_statement = iam.PolicyStatement(
            actions=["dynamodb:PutItem"],
            resources=[loginevents_table.table_arn]
        )

        # create a lambda function "write_to_login_events"
        write_to_login_events = _lambda.Function(
            self, 'WriteToLoginEventsHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='write_to_login_events.write_to_login_events',
            initial_policy=[write_to_login_events_policy_statement],
            environment={"loginevents_table": loginevents_table.table_arn}
        )

        # create an iam policy statement to allow lambda function to write to logoutevents table
        write_to_logout_events_policy_statement = iam.PolicyStatement(
            actions=["dynamodb:PutItem"],
            resources=[logoutevents_table.table_arn]
        )

        # create a lambda function "write_to_logout_events"
        write_to_logout_events = _lambda.Function(
            self, 'WriteToLogoutEventsHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='write_to_logout_events.write_to_logout_events',
            initial_policy=[write_to_logout_events_policy_statement],
            environment={"logoutevents_table": logoutevents_table.table_arn}
        )

        state_machine = sf.CfnStateMachine(
            self, 'AccessControlStateMachine',
            role_arn='arn:aws:iam::821383200340:role/service-role/StepFunctions-AccessControlCheckV2-role-814f6a0a',
            state_machine_name='AccessControlStateMachineCDK',
            definition_string='''{
               "Comment":"RFID tag read state machine",
               "StartAt":"StartUserAuthentication",
               "States":{
                  "StartUserAuthentication":{
                     "Type":"Parallel",
                     "Next":"EvaluateInitialAuthentication",
                     "Branches":[
                        {
                           "StartAt":"CheckForUserInPersonTable",
                           "States":{
                              "CheckForUserInPersonTable":{
                                 "Type":"Task",
                                 "Resource":"%s",
                                 "End":true
                              }
                           }
                        },
                        {
                           "StartAt":"CompareFaces",
                           "States":{
                              "CompareFaces":{
                                 "Type":"Task",
                                 "Resource":"%s",
                                 "Next":"IsFaceInS3?"
                              },
                              "IsFaceInS3?":{
                                 "Type":"Choice",
                                 "Choices":[
                                    {
                                       "Not":{
                                          "Variable":"$.face",
                                          "StringEquals":"notavailable"
                                       },
                                       "Next":"ParseRekognitionResponse"
                                    },
                                    {
                                       "Variable":"$.face",
                                       "StringEquals":"notavailable",
                                       "Next":"GenerateRekognitionResponse"
                                    }
                                 ],
                                 "Default":"ChoiceErrorState1"
                              },
                              "ParseRekognitionResponse":{
                                 "Type":"Task",
                                 "Resource":"%s",
                                 "Next":"GenerateRekognitionResponse"
                              },
                              "GenerateRekognitionResponse":{
                                 "Type":"Task",
                                 "Resource":"%s",
                                 "End":true
                              },
                              "ChoiceErrorState1":{
                                 "Type":"Fail",
                                 "Cause":"No Matches!"
                              }
                           }
                        }
                     ]
                  },
                  "EvaluateInitialAuthentication":{
                     "Type":"Task",
                     "Resource":"%s",
                     "Next":"LoginSuccessful?"
                  },
                  "LoginSuccessful?":{
                     "Type":"Choice",
                     "Choices":[
                        {
                           "Variable":"$.state",
                           "StringEquals":"continue",
                           "Next":"CheckIfUserIsActive"
                        },
                        {
                           "Variable":"$.state",
                           "StringEquals":"failed",
                           "Next":"GenerateDBResponse"
                        }
                     ],
                     "Default":"ChoiceErrorState2"
                  },
                 "CheckIfUserIsActive":{
                                 "Type":"Task",
                                 "Resource":"%s",
                                 "Next":"IsUserActive?"
                              },
                              "IsUserActive?":{
                                 "Type":"Choice",
                                 "Choices":[
                                    {
                                       "Variable":"$.logout",
                                       "IsPresent":true,
                                       "Next":"RemoveUserFromActiveTable"
                                    },
                                    {
                                       "Variable":"$.login",
                                       "IsPresent":true,
                                       "Next":"CheckForConcurrentUsers"
                                    }
                                 ],
                                 "Default":"ChoiceErrorState2"
                              },
                              "CheckForConcurrentUsers":{
                                 "Type":"Task",
                                 "Resource":"%s",
                                 "Next":"CheckUserCount"
                              },
                              "CheckUserCount":{
                                 "Type":"Choice",
                                 "Choices":[
                                    {
                                       "Variable":"$.usercount",
                                       "NumericLessThan":10,
                                       "Next":"AddUserToActiveTable"
                                    },
                                    {
                                       "Variable":"$.usercount",
                                       "NumericGreaterThanEquals":10,
                                       "Next":"GenerateDBResponse"
                                    }
                                 ],
                                 "Default":"ChoiceErrorState2"
                              },
                              "RemoveUserFromActiveTable":{
                                 "Type":"Task",
                                 "Resource":"%s",
                                 "Next":"GenerateDBResponse"
                              },
                              "AddUserToActiveTable":{
                                 "Type":"Task",
                                 "Resource":"%s",
                                 "Next":"GenerateDBResponse"
                              },
                              "GenerateDBResponse":{
                                 "Type":"Task",
                                 "Resource":"%s",
                                 "Next":"EvaluateAuthenticationResponse"
                              },
                               "ChoiceErrorState2":{
                                 "Type":"Fail",
                                 "Cause":"No Matches!"
                              },
                 "EvaluateAuthenticationResponse":{
                     "Type":"Task",
                     "Resource":"%s",
                     "Next": "WhichEventDBToWrite?"
                },
                 "WhichEventDBToWrite?":{
                     "Type":"Choice",
                     "Choices":[
                           { "And": [
                           {
                           "Variable":"$.state",
                           "StringEquals":"login"
                           },
                           {
                           "Variable":"$.response.access",
                           "StringEquals":"allow"
                           }
                          ],
                           "Next":"WriteToLoginEvents"
                          },
                          { "And": [
                           {
                           "Variable":"$.state",
                           "StringEquals":"logout"
                           },
                           {
                           "Variable":"$.response.access",
                           "StringEquals":"allow"
                           }
                          ],
                           "Next":"WriteToLogoutEvents"
                         },
                        {
                           "Variable":"$.response.access",
                           "StringEquals":"deny",
                           "Next":"WriteToDeniedLoginTable"
                        }
                     ]
                 },
                 "WriteToLoginEvents":{
                     "Type":"Task",
                     "Resource":"%s",
                     "Next": "PublishToIoTTopic"
                },
                 "WriteToLogoutEvents":{
                     "Type":"Task",
                     "Resource":"%s",
                     "Next": "PublishToIoTTopic"
                },
                 "WriteToDeniedLoginTable":{
                     "Type":"Task",
                     "Resource":"%s",
                     "Next": "PublishToIoTTopic"
                },
                 "PublishToIoTTopic":{
                     "Type":"Task",
                     "Resource":"%s",
                     "End": true
                }
            }
            }''' % (check_for_user_in_persontable.function_arn,
                    compare_faces.function_arn,
                    parse_rekognition_response.function_arn,
                    generate_rekognition_response.function_arn,
                    evaluate_initial_authentication.function_arn,
                    check_if_user_is_active.function_arn,
                    check_for_concurrent_users.function_arn,
                    activetable_remove_user.function_arn,
                    activetable_put_user.function_arn,
                    generate_db_response.function_arn,
                    evaluate_authentication_response.function_arn,
                    write_to_login_events.function_arn,
                    write_to_logout_events.function_arn,
                    write_to_failedlogins.function_arn,
                    publish_to_iot_topic.function_arn
                    )
            )

        # create an iam policy statement to allow lambda function to step functions state machine execution
        start_state_machine_policy_statement = iam.PolicyStatement(
            actions=["states:StartExecution"],
            resources=["*"]
        )

        region = core.Environment(region='Aws.region')
        accountid = core.Environment(account='Aws.accountId')

        # create a lambda function "start_state_machine"
        start_state_machine = _lambda.Function(
            self, 'StartStateMachineHandler',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='start_dbcheck_state_machine.start_state_machine',
            initial_policy=[start_state_machine_policy_statement],
            environment={"state_machine": f"arn:aws:states:{region}:{accountid}:stateMachine:{state_machine.state_machine_name}"}

        )
        self._capture_bucket.add_event_notification(s3.EventType.OBJECT_CREATED_PUT,
                                            notifications.LambdaDestination(start_state_machine))

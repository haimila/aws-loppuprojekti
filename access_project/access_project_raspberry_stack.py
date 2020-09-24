from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    aws_sns as sns,
    core
)


class RaspberryStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, bucket: s3.Bucket, capture_bucket: s3.Bucket,
                 write_topic: sns.Topic, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create an iam user "RaspberryPiUser"
        rasberry_pi_user = iam.User(
            self, "RaspberryPiUser",
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodeCommitPowerUser"),
                              iam.ManagedPolicy.from_aws_managed_policy_name("AWSIoTFullAccess")
                              ]
        )

        # create an iam policy statement for "WriteToS3Policy"
        write_to_s3_policy_statement = iam.PolicyStatement(
            actions=["s3:PutObject"],
            resources=[bucket.bucket_arn,
                       capture_bucket.bucket_arn]
        )

        # create an iam policy "WriteToS3Policy"
        write_to_s3_policy = iam.Policy(
            self, "WriteToS3Policy",
            statements=[write_to_s3_policy_statement],
            users=[rasberry_pi_user]
        )

        # create an iam policy statement to allow RaspberryPiUser to publish to sns topic
        publish_to_sns_topic_policy_statement = iam.PolicyStatement(
            actions=["sns:Publish"],
            resources=[write_topic.topic_arn]
        )

        # create an iam policy "PublishToSnsTopic"
        publish_to_sns_topic_policy = iam.Policy(
            self, "PublishToSnsTopicPolicy",
            statements=[publish_to_sns_topic_policy_statement],
            users=[rasberry_pi_user]
        )
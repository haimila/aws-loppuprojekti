from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    core
)

class RaspberryStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, bucket: s3.Bucket, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        write_to_s3_policy_statement = iam.PolicyStatement(
            sid="VisualEditor0",
            actions=["s3:PutObject"],
            resources=[bucket.bucket_arn]
        )

        rasberry_pi_user = iam.User(
            self, "RaspberryPiUser",
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodeCommitPowerUser"),
                              iam.ManagedPolicy.from_aws_managed_policy_name("AWSIoTFullAccess")
                              ]
        )

        write_to_s3_policy = iam.Policy(
            self, "WriteToS3Policy",
            statements=[write_to_s3_policy_statement],
            users=[rasberry_pi_user]
        )
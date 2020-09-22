from aws_cdk import (
    aws_iam as iam,
    core
)


class RaspberryStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        rasberry_pi_user = iam.User(
            self, "RaspberryPiUser",
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodeCommitPowerUser"),
                              iam.ManagedPolicy.from_aws_managed_policy_name("AWSIoTFullAccess"),
                              iam.ManagedPolicy.from_aws_managed_policy_name("RaspberryPiWriteS3AccessProjectBuckets")]
        )
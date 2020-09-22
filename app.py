#!/usr/bin/env python3

from aws_cdk import core

from access_project.access_project_stack import AccessProjectStack
from access_project.access_project_database_stack import DatabaseStack
from access_project.access_project_raspberry_stack import RaspberryStack


app = core.App()
accessStack = AccessProjectStack(app, "access-project")
DatabaseStack(app, "access-project-database")
RaspberryStack(app, "access-project-raspberry", bucket=accessStack.bucket)

app.synth()

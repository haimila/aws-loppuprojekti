#!/usr/bin/env python3

from aws_cdk import core

from access_project.access_project_stack import AccessProjectStack


app = core.App()
AccessProjectStack(app, "access-project")

app.synth()

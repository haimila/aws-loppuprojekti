#!/usr/bin/env python3

from aws_cdk import core

from access_project.access_project_stack import AccessProjectStack
from access_project.access_project_database_stack import DatabaseStack


app = core.App()
AccessProjectStack(app, "access-project")
DatabaseStack(app, "access-project-database")

app.synth()

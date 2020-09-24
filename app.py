#!/usr/bin/env python3

from aws_cdk import core

from access_project.access_project_stack import AccessProjectStack
from access_project.access_project_database_stack import DatabaseStack
from access_project.access_project_raspberry_stack import RaspberryStack


app = core.App()
databaseStack = DatabaseStack(app, "access-project-database")
accessStack = AccessProjectStack(app, "access-project",
                                 active_table=databaseStack.active_table,
                                 person_table=databaseStack.person_table,
                                 failedlogins_table=databaseStack.failedlogins_table,
                                 loginevents_table=databaseStack.loginevents_table,
                                 logoutevents_table=databaseStack.logoutevents_table)
RaspberryStack(app, "access-project-raspberry", bucket=accessStack.bucket)

app.synth()

from flask import Flask
from flask.ext.migrate import Migrate, Manager, MigrateCommand
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Imports
from main import models
from main import views
from rest import RestHelloWorld

# setup RESTful API
api.add_resource(RestHelloWorld, '/rest/api/hello')

# used to manage the app
manager = Manager(app)

# adds the db commands to the runserver.py
# 
# db init - creates all db tables
# db migrate - create migrations scripts to make any new changes to schema
# db upgrade - runs migrations scripts to implement new schema changes
manager.add_command('db', MigrateCommand)
from flask import Flask
from flask.ext.migrate import Migrate, Manager, MigrateCommand
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#used for sse push events
subscriptions = []

# Imports
from main import models
from main import views
from main.rest import RestHelloWorld, RestNode, RestNodeList, RestNodeGoals,\
    RestNodeLocation, RestNodeJumpPoints, RestObstacles, RestNodeForces

# setup RESTful API
api.add_resource(RestHelloWorld, '/rest/api/hello')
api.add_resource(RestNodeList, '/rest/api/nodes')
api.add_resource(RestNode, '/rest/api/nodes/<int:node_id>')
api.add_resource(RestNodeGoals, '/rest/api/nodes/<int:node_id>/goals')
api.add_resource(RestNodeLocation, '/rest/api/nodes/<int:node_id>/location')
api.add_resource(RestNodeForces, '/rest/api/nodes/<int:node_id>/force')
api.add_resource(RestNodeJumpPoints, '/rest/api/nodes/<int:node_id>/jumppoints')
api.add_resource(RestObstacles, '/rest/api/obstacles')



# used to manage the app
manager = Manager(app)

# adds the db commands to the runserver.py
# 
# db init - creates all db tables
# db migrate - create migrations scripts to make any new changes to schema
# db upgrade - runs migrations scripts to implement new schema changes
manager.add_command('db', MigrateCommand)
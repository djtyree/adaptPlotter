###################################################################
#################             IMPORTS           ###################
###################################################################
from flask.ext.restful import Resource

# model imports

# function imports

from main import app

###################################################################


class RestHelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
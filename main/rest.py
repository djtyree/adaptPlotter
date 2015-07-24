###################################################################
#################             IMPORTS           ###################
###################################################################
from flask.ext.restful import Resource, reqparse
from flask import jsonify
# model imports
from models import Node

# function imports

###################################################################


class RestHelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

def jsonNode(node):
    if node.leader_id == 0:
        leader = "True"
        leader_id = node.id
    else:
        leader = "False"
        leader_id = node.leader_id
    return {
            'id': node.id, 
            'name': node.name,
            'latitude': node.location.lat,
            'longitude': node.location.lon,
            'is_leader': leader,
            'leader_id': leader_id,
            'jumppoints': node.getJumpPoints(),
            'goals': node.getGoals()
            }

# RestNode
# works with a single node    
class RestNode(Resource):              
    def get(self, node_id):
        node = None        
        nodes = Node.query.all()    # @UndefinedVariable
        
        if nodes:
            for x in nodes:
                if x.id == node_id:
                    node = x                    
            if node:
                return jsonNode(node)
            
# RestNodeList
# works with all nodes    
class RestNodeList(Resource):
    def get(self):        
        nodes = Node.query.all()    # @UndefinedVariable
        nodeList = {}
        for node in nodes:
            nodeList[node.id] = jsonNode(node)
        return nodeList
            
        
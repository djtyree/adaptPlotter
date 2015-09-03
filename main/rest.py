###################################################################
#################             IMPORTS           ###################
###################################################################
from flask import jsonify
from flask.ext.restful import Resource, reqparse

from main import db
from models import Node


# model imports
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
            'nid': node.id,
            'rid': node.rid, 
            'name': node.name,
            'latitude': node.location.lat,
            'longitude': node.location.lon,
            'is_leader': leader,
            'leader_id': leader_id,
            'jumppoints': node.getJumpPoints(),
            'goals': node.getGoals()
            }
def jsonNodeGoal(node):
    return node.getGoals() 

# RestNode
# works with a single node    
class RestNode(Resource):              
    def get(self, node_id):
        node = None        
        nodes = Node.query.all()    # @UndefinedVariable
        
        if nodes:
            for x in nodes:
                if x.rid == node_id:
                    node = x                    
            if node:
                return jsonNode(node)
            
            # RestNode
            
# works with a single node    
class RestNodeGoals(Resource):              
    def get(self, node_id):
        node = None        
        nodes = Node.query.all()    # @UndefinedVariable
        
        if nodes:
            for x in nodes:
                if x.rid == node_id:
                    node = x                    
            if node:
                return {'goals': jsonNodeGoal(node)}
            
# RestNodeList
# works with all nodes    
class RestNodeList(Resource):
    def get(self):        
        nodes = Node.query.all()    # @UndefinedVariable
        nodeList = {'nodes': []}
        for node in nodes:
            nodeList['nodes'].append(jsonNode(node));
        return nodeList
            
# RestLocation
class RestNodeLocation(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('lat')
        self.reqparse.add_argument('lon')        
        super(RestNodeLocation, self).__init__()
        
    def get(self, node_id):
        node = None        
        nodes = Node.query.all()    # @UndefinedVariable
        
        if nodes:
            for x in nodes:
                if x.rid == node_id:
                    node = x                    
            if node:
                return { 'currentLocation': {
                                             'lat': node.location.lat,
                                             'lon': node.location.lon,
                                             } 
                        }
            
    def put(self, node_id):        
        node = None
        nodes = Node.query.all()    # @UndefinedVariable
        for x in nodes:
            if x.id == node_id:
                node = x
        if node:
            args = self.reqparse.parse_args()
            lat = args['lat']
            lon = args['lon']
            node.location.lat = float(lat)
            node.location.lon = float(lon)
            db.session.commit()
            return {
                    'result': {
                               'node': node.name,
                               'nid': node.id,
                               'id': node.rid,
                               'lat': node.location.lat, 
                               'lon': node.location.lon, 
                               'msg': 'New location correctly set' 
                               }
                    }
# RestLocation
class RestNodeJumpPoints(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('lat')
        self.reqparse.add_argument('lon')        
        super(RestNodeLocation, self).__init__()
        
    def get(self, node_id):
        node = None        
        nodes = Node.query.all()    # @UndefinedVariable
        
        if nodes:
            for x in nodes:
                if x.rid == node_id:
                    node = x                    
            if node:
                return { 'currentLocation': {
                                             'lat': node.location.lat,
                                             'lon': node.location.lon,
                                             } 
                        }
            
    def put(self, node_id):        
        node = None
        nodes = Node.query.all()    # @UndefinedVariable
        for x in nodes:
            if x.id == node_id:
                node = x
        if node:
            args = self.reqparse.parse_args()
            lat = args['lat']
            lon = args['lon']
            node.location.lat = float(lat)
            node.location.lon = float(lon)
            db.session.commit()
            return {
                    'result': {
                               'node': node.name,
                               'nid': node.id,
                               'id': node.rid,
                               'lat': node.location.lat, 
                               'lon': node.location.lon, 
                               'msg': 'New location correctly set' 
                               }
                    }
                        
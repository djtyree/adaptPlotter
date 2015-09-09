###################################################################
#################             IMPORTS           ###################
###################################################################
import unicodedata

from flask import make_response, json
from flask.ext.restful import Resource, reqparse

from main import db
from main.models import JumpPoint, Location
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
        self.reqparse.add_argument('jps')       
        super(RestNodeJumpPoints, self).__init__()
        
    def get(self, node_id):
        node = None        
        nodes = Node.query.all()    # @UndefinedVariable
        
        if nodes:
            for x in nodes:
                if x.rid == node_id:
                    node = x                    
            if node:
                return { 'jptest': {
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
            data = args['jps']
            jp_data = json.loads(data)
            
            node_jumppoints = node.jumppoints
            
            for node_jp in node.jumppoints:
                db.session.delete(node_jp)
                
            for jp in jp_data:
                
                new_jp = JumpPoint()

                lat = float(jp['lat'])
                lon = float(jp['lng'])
                location = Location(lat=lat, lon=lon)
                db.session.add(location)  # @UndefinedVariable
                
                new_jp.location = location
                new_jp.position = len(node.jumppoints) + 1
                new_jp.goal = 0
                # check if jumppoint should be listed as a goal
                for node_jp in node_jumppoints:
                    node_jp_lat = node_jp.location.lat
                    node_jp_lon = node_jp.location.lon
                    if node_jp.goal and lat == node_jp_lat and lon == node_jp_lon:
                        new_jp.goal = 1
                        
                node.jumppoints.append(new_jp)
            db.session.commit()
            return {
                    'result': {
                               'node': node.name,
                               'nid': node.id,
                               'id': node.rid, 
                               'msg': 'Test' 
                               }
                    }
                        
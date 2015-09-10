###################################################################
#################             IMPORTS           ###################
###################################################################
from flask import json
from flask.ext.restful import Resource, reqparse

from main import db

# model imports
from models import Node, JumpPoint, Location, Obstacle

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
# RestObstacles
class RestObstacles(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('obstacles')       
        super(RestObstacles, self).__init__()
        
    def get(self):
        obs = Obstacle.query.all()    # @UndefinedVariable
        obList = {'obstacles': []}
        for ob in obs:
            obList['obstacles'].append({'id': ob.id, 'lat': ob.location.lat, 'lon': ob.location.lon});
        return obList
            
    def put(self):            
        args = self.reqparse.parse_args()
        data = args['obstacles']
        ob_data = json.loads(data)
            
        newObCount = 0
        for ob in ob_data:  
                                  
            lat = float(ob['lat'])
            lon = float(ob['lon'])
            obExists = False
            existingLocation = Location.query.filter_by(lat=lat,lon=lon).first() # @UndefinedVariable
            if existingLocation is not None:
                # something is already at this location. see if it is an obstacle
                existingObstacle = Obstacle.query.filter_by(loc_id=existingLocation.id) # @UndefinedVariable
                if existingObstacle is not None:
                    obExists = True
            
            # create new obstacle only if one doesn't already exist
            if not obExists:
                newOb = Obstacle()
                newLocation = Location(lat=lat, lon=lon)
                db.session.add(newLocation)  # @UndefinedVariable
                db.session.commit()
                newOb.location = newLocation
                db.session.add(newOb)  # @UndefinedVariable
                newObCount = newObCount + 1
                
        db.session.commit()
                    
        return {
                'result': {                           
                           'msg': str(newObCount) + " obstacles created." 
                           }
                }
                                            
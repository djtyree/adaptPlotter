###################################################################
#################             IMPORTS           ###################
###################################################################
from flask import json
from flask.ext.restful import Resource, reqparse

from main import db

# model imports
from models import Node, JumpPoint, Location, Obstacle, Goal

# function imports
from views import publish_events

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
    def __init__(self):
        self.reqparse = reqparse.RequestParser()     
        self.reqparse.add_argument('lat')
        self.reqparse.add_argument('lon')
        self.reqparse.add_argument('position')
                      
    def get(self, node_id):
        node = None        
        nodes = Node.query.all()    # @UndefinedVariable
        
        if nodes:
            for x in nodes:
                if x.rid == node_id:
                    node = x                    
            if node:
                return {'goals': jsonNodeGoal(node)}
    def put(self, node_id):
        node = None        
        nodes = Node.query.all()    # @UndefinedVariable
        
        if nodes:
            for x in nodes:
                if x.rid == node_id:
                    node = x                    
            if node:
                args = self.reqparse.parse_args()
                new_lat = args['lat']
                new_lon = args['lon']
                new_pos = args['position']
                location = Location(lat=new_lat, lon=new_lon)
                db.session.add(location)  # @UndefinedVariable
                
                exisiting_goal_id = 0
                existing_goal = None
                for goal in node.goals:
                    old_pos = goal.position
                    if int(old_pos) == (int(new_pos)+1):
                        exisiting_goal_id = goal.id
                        exisiting_goal = goal
                
                if exisiting_goal_id != 0:
                    db.session.delete(exisiting_goal)
                
                newgoal = Goal()
                newgoal.location = location
                newgoal.position = int(new_pos) + 1            
                db.session.add(newgoal)
                node.goals.append(newgoal)
                db.session.commit()
                
                return {'new_goals': jsonNodeGoal(node)}
        
                    
            
# RestNodeList
# works with all nodes    
class RestNodeList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name')
        self.reqparse.add_argument('rid')
        self.reqparse.add_argument('ip')
        self.reqparse.add_argument('leader')     
        self.reqparse.add_argument('lat')
        self.reqparse.add_argument('lon')
            
    def get(self):        
        nodes = Node.query.all()    # @UndefinedVariable
        nodeList = {'nodes': []}
        for node in nodes:
            nodeList['nodes'].append(jsonNode(node));
        return nodeList
    
    def put(self):
        args = self.reqparse.parse_args()        
        node = None
        nodes = Node.query.all()    # @UndefinedVariable
        node_id = args['rid']
        for x in nodes:
            if x.rid == node_id:
                node = x
        if node:
                return {
                    'result': {
                               'nid': node.id,
                               'id': node.rid,                                
                               'msg': 'Robot with that id already exists!' 
                               }
                    }
        else:
            new_ip = args['ip']
            new_lat = args['lat']
            new_lon = args['lon']
            new_leader_rid = args['leader']
            new_name = args['name']
            new_leader = 0
            if new_leader_rid != 0:
                for x in nodes:
                    if x.id == new_leader_rid:
                        new_leader = x.id
            
            
            #new node has passed validation, add to db
            location = Location(lat=new_lat, lon=new_lon)
            db.session.add(location)  # @UndefinedVariable
            node = Node(name=new_name, leader_id=new_leader, location=location, rid=node_id, ip=new_ip)
            db.session.add(node)  # @UndefinedVariable
            db.session.commit()  # @UndefinedVariable
            publish_events(reqType="newNode", rid=node_id)
             
            return {
                    'result': {
                               'node': node.name,
                               'nid': node.id,
                               'id': node.rid,                                
                               'msg': 'Node Added' 
                               }
                    }
             

# RestGoalComplete
class RestGoalComplete(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('lat')
        self.reqparse.add_argument('lon')         
        super(RestGoalComplete, self).__init__()
            
    def put(self, node_id):        
        node = None
        nodes = Node.query.all()    # @UndefinedVariable
        for x in nodes:
            if x.rid == node_id:
                node = x
        if node:
            args = self.reqparse.parse_args()
            lat = args['lat']
            lon = args['lon']
            for goal in node.goals:
                if str(goal.location.lat) == str(lat) and str(goal.location.lon) == str(lon):
                    db.session.delete(goal)
                    db.session.commit()
                    publish_events(reqType="goalComplete", rid=node_id)
                    break
            
            return {
                    'result': {
                               'node': node.name,
                               'nid': node.id,
                               'id': node.rid,                                
                               'msg': 'Goal Successfully Removed' 
                               }
                    }
            
# RestLocation
class RestNodeLocation(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('lat')
        self.reqparse.add_argument('lon')
        self.reqparse.add_argument('speed')     
        self.reqparse.add_argument('dir')             
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
                                             'speed': node.location.speed,
                                             'dir': node.location.dir
                                             } 
                        
                        }
            
    def put(self, node_id):        
        node = None
        nodes = Node.query.all()    # @UndefinedVariable
        for x in nodes:
            if x.rid == node_id:
                node = x
        if node:
            args = self.reqparse.parse_args()
            lat = args['lat']
            lon = args['lon']
            speed = args['speed']
            dir = args['dir']
            #print "Location: lat=" + str(lat) + " lon=" + str(lon)
            #if speed is not None:
            #    print "   - speed= " + str(speed)
            #if dir is not None:
            #    print "   - dir= " + str(dir)
            
                      
            node.location.lat = float(lat)
            node.location.lon = float(lon)
            if speed is not None:
                node.location.speed = float(speed)
            if dir is not None:    
                node.location.dir = float(dir)
            db.session.commit()
            publish_events(reqType="nodeLocation", rid=node_id)
            
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
# RestForces
class RestNodeForces(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('force_speed')
        self.reqparse.add_argument('force_dir')        
        super(RestNodeForces, self).__init__()
        
    def get(self, node_id):
        node = None        
        nodes = Node.query.all()    # @UndefinedVariable
        
        if nodes:
            for x in nodes:
                if x.rid == node_id:
                    node = x                    
            if node:
                return { 'forceVector': {
                                             'force_speed': node.force_speed,
                                             'force_dir': node.force_dir,
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
            fspeed = args['force_speed']
            fdir = args['force_dir']
            print "Force: speed=" + fspeed + " dir=" + fdir
            node.force_speed = float(fspeed)
            node.force_dir = float(fdir)
            db.session.commit()
            return {
                    'result': {
                               'node': node.name,
                               'nid': node.id,
                               'id': node.rid,
                               'force_speed': node.force_speed, 
                               'force_dir': node.force_dir, 
                               'msg': 'New force vector correctly set' 
                               }
                    }
                        
# RestNodeJumpPoints
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
            #print "JumpPoints: " + data
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
                        
                node.jumppoints.append(new_jp)
            db.session.commit()
            publish_events(reqType="nodeJumpPoints", rid=node_id)
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
        print "Obstacles" + data
        newObCount = 0
        for ob in ob_data:  
                                  
            lat = float(ob['lat'])
            lon = float(ob['lon'])
            obExists = False
            existingLocation = Location.query.filter_by(lat=lat,lon=lon).first() # @UndefinedVariable
            if existingLocation is not None:
                # something is already at this location. see if it is an obstacle
                existingObstacle = Obstacle.query.filter_by(loc_id=existingLocation.id).first() # @UndefinedVariable
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
                publish_events(reqType="newObstacle", lat=lat, lon=lon)
                
        db.session.commit()
                    
        return {
                'result': {                           
                           'msg': str(newObCount) + " obstacles created." 
                           }
                }
                                            
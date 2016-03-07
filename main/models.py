from main import db

from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_utils import auto_delete_orphans

node_jump_association_table = db.Table('node_jp_association',
    db.Column('node_id', db.Integer, db.ForeignKey('node.id')),
    db.Column('jumppoint_id', db.Integer, db.ForeignKey('jumppoint.id'))
)

node_goal_association_table = db.Table('node_goal_association',
    db.Column('node_id', db.Integer, db.ForeignKey('node.id')),
    db.Column('goal_id', db.Integer, db.ForeignKey('goal.id'))
)

# Location Class
class Location(db.Model):
    # table name
    __tablename__ = 'location'
    
    # columns
    id = db.Column(db.Integer(), primary_key=True)
    lat = db.Column(db.Float)    
    lon = db.Column(db.Float) 
    speed = db.Column(db.Float, default=0.0) 
    dir = db.Column(db.Float, default=0.0)          

    # class functions
    def __repr__(self):
        return '<Location %d - lat: %f, lon: %f, dir: %f, speed: %f>' % (self.id, self.lat, self.lon, self.dir, self.speed)

# Node Class    
class Node(db.Model):
    # table name
    __tablename__ = 'node'
    
    # columns
    id = db.Column(db.Integer(), primary_key=True)
    rid = db.Column(db.Integer())
    name = db.Column(db.String(64))
    ip = db.Column(db.String(64))
    leader_id = db.Column(db.Integer(), db.ForeignKey('node.id'))    
    loc_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    force_dir = db.Column(db.Float, default=0.0) 
    force_speed = db.Column(db.Float, default=0.0)  
    
    # relationships
    location = db.relationship("Location",backref=db.backref("node", uselist=False), cascade="all, delete-orphan", single_parent=True)
    followers = db.relationship("Node",backref=db.backref("leader", remote_side='Node.id'), foreign_keys='Node.leader_id')
    jumppoints = db.relationship('JumpPoint', order_by="JumpPoint.position", collection_class=ordering_list('position'), secondary=node_jump_association_table, backref='nodes')
    goals = db.relationship('Goal', order_by="Goal.position", collection_class=ordering_list('position'), secondary=node_goal_association_table, backref='nodes')
    
    # inheritance
    
    # class functions
    def isLeader(self):
        if self.leader_id == 0:
            return True
        else:
            return False
    
    def __repr__(self):
        return '<Node %s>' % (self.name)
    
    def getJumpPoints(self):
        jps = {}
        for jp in self.jumppoints:            
            jps[jp.id] = jp.getJSON()
        return jps
    
    def getGoals(self):
        goals = []
        for goal in self.goals:      
            goals.append(goal.getJSON())
        return goals
     
# Point Class
class JumpPoint(db.Model):
    # table name
    __tablename__ = 'jumppoint'
    
    # columns
    id = db.Column(db.Integer(), primary_key=True)
    position = db.Column(db.Integer())
    loc_id = db.Column(db.Integer(), db.ForeignKey('location.id'))    
    
    # relationships
    location = db.relationship("Location",backref=db.backref("jumppoint", uselist=False), cascade="all, delete-orphan", single_parent=True)
    
    # class functions
    def __repr__(self):
        return '<Point %d>' % (self.id)
    
    def getJSON(self):
        json = { "position": self.position,
                 "lat": self.location.lat,
                 "lon": self.location.lon
                }
        return json

# Point Class
class Goal(db.Model):
    # table name
    __tablename__ = 'goal'
    
    # columns
    id = db.Column(db.Integer(), primary_key=True)
    position = db.Column(db.Integer())
    loc_id = db.Column(db.Integer(), db.ForeignKey('location.id'))    
    
    # relationships
    location = db.relationship("Location",backref=db.backref("goal", uselist=False), cascade="all, delete-orphan", single_parent=True)
        
    def __repr__(self):
        return '<Point %d>' % (self.id)
    
    def getJSON(self):
        json = { "position": self.position,
                 "lat": self.location.lat,
                 "lon": self.location.lon
                }
        return json
    
    
# Obstacle Class
class Obstacle(db.Model):
    # table name
    __tablename__ = 'obstacle'
    
    # columns
    id = db.Column(db.Integer(), primary_key=True)
    loc_id = db.Column(db.Integer(), db.ForeignKey('location.id'))
    
    # relationships
    location = db.relationship("Location",backref=db.backref("obstacle", uselist=False), cascade="all, delete-orphan", single_parent=True)
    
    # inheritance
    
    # class functions
    def __repr__(self):
        return '<Obstacle %d>' % (self.id)

auto_delete_orphans(Node.jumppoints)    
auto_delete_orphans(Node.goals)    
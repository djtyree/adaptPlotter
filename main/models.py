from main import db

from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_utils import auto_delete_orphans
from sqlalchemy.orm.strategies import single_parent_validator

node_jump_association_table = db.Table('node_jp_association',
    db.Column('node_id', db.Integer, db.ForeignKey('node.id')),
    db.Column('jumppoint_id', db.Integer, db.ForeignKey('jumppoint.id'))
)

# Location Class
class Location(db.Model):
    # table name
    __tablename__ = 'location'
    
    # columns
    id = db.Column(db.Integer(), primary_key=True)
    lat = db.Column(db.Float)    
    lon = db.Column(db.Float)          

    # class functions
    def __repr__(self):
        return '<Location %d - lat: %f, lon: %f>' % (self.id, self.lat, self.lon)

# Node Class    
class Node(db.Model):
    # table name
    __tablename__ = 'node'
    
    # columns
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64))
    leader_id = db.Column(db.Integer(), db.ForeignKey('node.id'))    
    loc_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    
    # relationships
    location = db.relationship("Location",backref=db.backref("node", uselist=False), cascade="all, delete-orphan", single_parent=True)
    followers = db.relationship("Node",backref=db.backref("leader", remote_side='Node.id'), foreign_keys='Node.leader_id')
    jumppoints = db.relationship('JumpPoint', order_by="JumpPoint.position", collection_class=ordering_list('position'), secondary=node_jump_association_table, backref='nodes')
    
    # inheritance
    
    # class functions
    def isLeader(self):
        if self.leader_id == 0:
            return True
        else:
            return False
    
    def __repr__(self):
        return '<Object %s>' % (self.name)
    
    def getJumpPoints(self):
        jps = {}
        for jp in self.jumppoints:            
            jps[jp.id] = jp.getJSON()
        return jps
    
    def getGoals(self):
        jps = {}
        for jp in self.jumppoints:
            if jp.isGoal():            
                jps[jp.id] = jp.getJSON()
        return jps
     
# Point Class
class JumpPoint(db.Model):
    # table name
    __tablename__ = 'jumppoint'
    
    # columns
    id = db.Column(db.Integer(), primary_key=True)
    position = db.Column(db.Integer())
    goal = db.Column(db.Boolean())
    loc_id = db.Column(db.Integer(), db.ForeignKey('location.id'))    
    
    # relationships
    location = db.relationship("Location",backref=db.backref("jumppoint", uselist=False), cascade="all, delete-orphan", single_parent=True)
    
    # class functions
    def isGoal(self):
        return self.goal
        
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
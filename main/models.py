from main import db

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

# Object Class
class Object(db.Model):
    # table name
    __tablename__ = 'object'
    
    # columns
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(50))      

    # inheritance
    __mapper_args__ = {
        'polymorphic_identity':'object',
        'polymorphic_on':type
    }
    
    # class functions
    def __repr__(self):
        return '<Object %d>' % (self.id)

# Node Class    
class Node(Object):
    # table name
    __tablename__ = 'node'
    
    # columns
    id = db.Column(db.Integer(), db.ForeignKey('object.id'), primary_key=True)
    name = db.Column(db.String(64))
    leader_id = db.Column(db.Integer(), db.ForeignKey('node.id'))
    followers = db.relationship("Node",backref=db.backref("leader", remote_side='Node.id'), foreign_keys='Node.leader_id')
    loc_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship("Location",backref=db.backref("node", uselist=False))
    
    # inheritance
    __mapper_args__ = {
        'polymorphic_identity':'node',
    }
    
    # class functions
    def isLeader(self):
        if self.leader_id == 0:
            return True
        else:
            return False
    
    def __repr__(self):
        return '<Object %s>' % (self.name)
    
# Point Class
class Point(Object):
    # table name
    __tablename__ = 'point'
    
    # columns
    id = db.Column(db.Integer(), db.ForeignKey('object.id'), primary_key=True)
    loc_id = db.Column(db.Integer(), db.ForeignKey('location.id'))
    
    # inheritance
    __mapper_args__ = {
        'polymorphic_identity':'point',
    }
    
    # class functions
    def __repr__(self):
        return '<Point %d>' % (self.id)
    
# Path Class
class Path(Object):
    # table name
    __tablename__ = 'path'
    
    # columns
    id = db.Column(db.Integer(), db.ForeignKey('object.id'), primary_key=True)
    loc_id = db.Column(db.Integer(), db.ForeignKey('location.id'))
    
    # relationships
    points = db.relationship('PathPoint', backref='path')
    
    # inheritance
    __mapper_args__ = {
        'polymorphic_identity':'path',
    }
    
    # class functions
    def __repr__(self):
        return '<Point %d>' % (self.id)
    
# Point Class
class PathPoint(db.Model):
    # table name
    __tablename__ = 'pathpoint'
    
    # columns
    id = db.Column(db.Integer(), primary_key=True)
    path_id = db.Column(db.Integer(), db.ForeignKey('path.id'))
    position = db.Column(db.Integer())
    loc_id = db.Column(db.Integer(), db.ForeignKey('location.id'))    
    
    # class functions
    def __repr__(self):
        return '<Point %d>' % (self.id)
    
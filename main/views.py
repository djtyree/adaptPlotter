from flask import render_template, jsonify, request, flash, redirect, url_for, json
from main import app, db
from models import Object, Node, Location, Point
from forms import NodeForm
import random
from main.forms import PointForm

@app.route('/')
def homePage():
    return render_template('home.html')

# Return Chart Data
@app.route('/data/random', methods=['GET'])
def getRandomData():    
    data = []
    count = random.randint(5,25)
    for x in range(0, count):
        data.append([random.randint(0,10), random.randint(0,10) ])
    
    return jsonify({'status':'OK','data':data})

# Return Chart Data
@app.route('/data/all', methods=['GET'])
def getAllData():    
    data = []
    objects = db.session.query(Object).all()
    leaders = Node.query.filter_by(leader_id=0).all()
    
    nodes = { 'name': 'Node', 'color': '#AAAAAA', 'data': [], 'marker': {'symbol': 'triangle', 'radius': 6} } 
    paths = { 'name': 'Paths', 'color': '#FF0000', 'data': [], 'marker': {'symbol': 'square', 'radius': 4} }
    points = { 'name': 'Points', 'color': '#00FF00', 'data': [], 'marker': {'symbol': 'circle', 'radius': 3} }
    
    for leader in leaders:
        nodes['data'].append(ChartPoint(x=leader.location.lat,y=leader.location.lon,color='#0000FF', name=leader.name,nid=leader.id, size=8).__dict__)
        for follower in leader.followers:
            nodes['data'].append(ChartPoint(x=follower.location.lat,y=follower.location.lon, name=follower.name,nid=follower.id,lid=leader.id).__dict__)
    for obj in objects:
        if obj.type == 'path':
            paths['data'].append(None)
        elif obj.type == 'point':    
            points['data'].append(ChartPoint(x=obj.location.lat,y=obj.location.lon,name='Point - ' + str(obj.id)).__dict__)
    data = [nodes, paths, points]
    return jsonify({'status':'OK','data':data})

# Node Add/Edit Page
@app.route('/node/add', defaults={'node_id': None}, methods=['GET', 'POST'])
@app.route('/node/<int:node_id>/edit', methods=['GET', 'POST'])
def addEditNode(node_id):    
    node = None
    # get choices for node leaders
    leader_choices = [(0, 'Self')]
    for x in Node.query.filter_by(leader_id=0):   # @UndefinedVariable
        leader_choices.append((x.id,x.name))
    form = NodeForm()
    form.leader.choices = leader_choices
    form.leader.default = 0    
    if node_id is not None:
        node = Node.query.get(node_id)
        
    if request.method == 'GET':
        if node is None:
            form.new.data = True
        else:
            form.new.data = False
            form.id.data = node.id
            form.name.data = node.name
            form.lat.data = node.location.lat
            form.lon.data = node.location.lon
            form.leader.data = node.leader_id    
    elif request.method == 'POST' and form.validate():  # @UndefinedVariable
        if node is None:
            #new node has passed validation, add to db
            location = Location(lat=form.lat.data, lon=form.lon.data)
            db.session.add(location)  # @UndefinedVariable
            node = Node(name=form.name.data, leader_id=form.leader.data, location=location)
            db.session.add(node)  # @UndefinedVariable
            db.session.commit()  # @UndefinedVariable
            flash("Node has beeen created")
        else: 
            #node has been updated. save updates
            node.name = form.name.data
            location = Location.query.get(node.loc_id)
            location.lat = form.lat.data
            location.lon = form.lon.data
            node.location = location
            node.leader_id = form.leader.data
            db.session.commit()  # @UndefinedVariable
            flash("Node has beeen updated")
            
        # after creating the new state, redirect them back to dce config page
        return redirect(url_for("nodePage"))    
    return render_template("nodeForm.html", form=form)

# Point Add/Edit Page
@app.route('/point/add', defaults={'point_id': None}, methods=['GET', 'POST'])
@app.route('/point/<int:point_id>/edit', methods=['GET', 'POST'])
def addEditPoint(point_id):
    point = None
    form = PointForm()  
    if point_id is not None:
        point = Point.query.get(point_id)
        
    if request.method == 'GET':
        if point is None:
            form.new.data = True
        else:  
            form.new.data = False    
            form.id.data = point.id
            form.lat.data = point.location.lat
            form.lon.data = point.location.lon    
    if request.method == 'POST' and form.validate():  # @UndefinedVariable
        if point is None:
            #new point has passed validation, add to db
            location = Location(lat=form.lat.data, lon=form.lon.data)
            db.session.add(location)  # @UndefinedVariable
            point= Point(location=location)
            db.session.add(point)  # @UndefinedVariable
            db.session.commit()  # @UndefinedVariable
            flash("Point has beeen created")
        else: 
            #node has been updated. save updates
            location = Location.query.get(point.loc_id)
            location.lat = form.lat.data
            location.lon = form.lon.data
            db.session.commit()  # @UndefinedVariable
            flash("Point has beeen updated")
        
        # after creating the new state, redirect them back to dce config page
        return redirect(url_for("pointPage"))    
    return render_template("pointForm.html", form=form)

# Node View page
@app.route('/node')
def nodePage():    
    nodes = Node.query.all()    # @UndefinedVariable   
    return render_template('nodes.html', nodes=nodes)

# Node View page
@app.route('/point')
def pointPage():    
    points = Point.query.all()    # @UndefinedVariable   
    return render_template('points.html', points=points)

#####################################################################
###                      Helper Functions                         ###
#####################################################################

class ChartPoint(object):
    nid = 0
    lid = 0
    x = 0
    y = 0
    color = ""
    name = ""
    marker = ""
    size=6
     
    def __init__(self, x, y, color=None, name=None, symbol=None, nid=None, lid=None, size=None):
        self.x = x
        self.y = y
        if nid is not None:
            self.nid = nid
        if lid is not None:
            self.lid = lid
        if color is not None:
            self.color = color
        if name is not None:
            self.name = name
        if symbol is not None or size is not None:
            self.marker = {}
            if symbol is not None:
                self.marker['symbol'] = symbol
            if size is not None:
                self.marker['radius'] = size

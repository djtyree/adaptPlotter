from flask import render_template, jsonify, request, flash, redirect, url_for, json
from main import app, db
from models import Object, Node, Location
from forms import NodeForm
import random

@app.route('/')
@app.route('/index')
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
    
    nodes = { 'name': 'Node', 'color': '#0000FF', 'data': [], 'marker': {'symbol': 'triangle'} } 
    paths = { 'name': 'Paths', 'color': '#0000FF', 'data': [], 'marker': {'symbol': 'square'} }
    points = { 'name': 'Points', 'color': '#00FF00', 'data': [], 'marker': {'symbol': 'circle'} }
    
    for obj in objects:
        if obj.type == 'node':
            if obj.isLeader():
                nodes['data'].append(ChartPoint(obj.location.lat,obj.location.lon,'#FF0000', obj.name,'triangle-down' ).__dict__)
            else:
                nodes['data'].append(ChartPoint(x=obj.location.lat,y=obj.location.lon, name=obj.name).__dict__)
        elif obj.type == 'path':
            paths['data'].append(None)
        elif obj.type == 'point':    
            points['data'].append(None)
    data = [nodes, paths, points]
    return jsonify({'status':'OK','data':data})

# Node Add/Edit Page
@app.route('/node/add', defaults={'node_id': None}, methods=['GET', 'POST'])
@app.route('/node/<int:node_id>/edit', methods=['GET', 'POST'])
def addEditNode(node_id):    
    if node_id is None:
        form = NodeForm(new=True)
    else:
        form = NodeForm(new=False)    
    leader_choices = [(0, 'Self')]
    for x in Node.query.all():   # @UndefinedVariable
        leader_choices.append((x.id,x.name))
    form.leader.choices = leader_choices
    form.leader.default = 0
    
    if request.method == 'POST' and form.validate():  # @UndefinedVariable
        #new node has passed validation, add to db
        location = Location(lat=form.lat.data, lon=form.lon.data)
        db.session.add(location)  # @UndefinedVariable
        node = Node(name=form.name.data, leader_id=form.leader.data, location=location)
        db.session.add(node)  # @UndefinedVariable
        db.session.commit()  # @UndefinedVariable
        flash("Node has beeen created")
        
        # after creating the new state, redirect them back to dce config page
        return redirect(url_for("nodePage"))    
    return render_template("nodeForm.html", form=form)

# Node View page
@app.route('/node')
def nodePage():    
    nodes = Node.query.all()    # @UndefinedVariable   
    return render_template('nodes.html', nodes=nodes)

#####################################################################
###                      Helper Functions                         ###
#####################################################################

class ChartPoint(object):
    x = 0
    y = 0
    color = ""
    name = ""
    marker = ""
     
    def __init__(self, x, y, color=None, name=None, marker=None):
        self.x = x
        self.y = y
        if color is not None:
            self.color = color
        if name is not None:
            self.name = name
        if marker is not None:
            self.marker = { 'symbol': marker}

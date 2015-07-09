from flask import render_template, jsonify, request, flash, redirect, url_for, json
from main import app, db
from models import Node, Location, Obstacle, JumpPoint
from forms import NodeForm, ObstacleForm
import random


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
    obstacles = db.session.query(Obstacle).all()
    leaders = Node.query.filter_by(leader_id=0).all()
    
    map_n = { 'name': 'Node', 'color': '#AAAAAA', 'data': [], 'marker': {'symbol': 'triangle', 'radius': 6}, 'zIndex': 3 } 
    map_jp = { 'lineWidth': 1,'name': 'Jump Points', 'color': '#FF0000', 'data': [], 'marker': {'symbol': 'square', 'radius': 2}, 'zIndex': 1 }
    map_o = { 'name': 'Obstacles', 'color': '#00FF00', 'data': [], 'marker': {'symbol': 'circle', 'radius': 3}, 'zIndex': 2 }
    
    for leader in leaders:
        map_n['data'].append(ChartPoint(x=leader.location.lat,y=leader.location.lon,color='#0000FF', name=leader.name,nid=leader.id, size=8).__dict__)
        map_jp['data'].append(ChartPoint(x=leader.location.lat,y=leader.location.lon, name='-', path=leader.id).__dict__)
        for jp in leaders.jumppoints:
            map_jp['data'].append(ChartPoint(x=jp.location.lat,y=jp.location.lon, name='Jump Point - ' + str(jp.id),pid=jp.id, node=leader.id).__dict__)
        for follower in leader.followers:
            map_n['data'].append(ChartPoint(x=follower.location.lat,y=follower.location.lon, name=follower.name,nid=follower.id,lid=leader.id).__dict__)
    for obj in obstacles:
        map_o['data'].append(ChartPoint(x=obj.location.lat,y=obj.location.lon,name='Point - ' + str(obj.id)).__dict__)

    data = [map_n, map_jp, map_o]
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
            form.location.lat.data = node.location.lat
            form.location.lon.data = node.location.lon
            form.leader.data = node.leader_id    
    elif request.method == 'POST' and form.validate():  # @UndefinedVariable
        if node is None:
            #new node has passed validation, add to db
            location = Location(lat=form.location.lat.data, lon=form.location.lon.data)
            db.session.add(location)  # @UndefinedVariable
            node = Node(name=form.name.data, leader_id=form.leader.data, location=location)
            db.session.add(node)  # @UndefinedVariable
            db.session.commit()  # @UndefinedVariable
            flash("Node has beeen created")
        else: 
            #node has been updated. save updates
            node.name = form.name.data
            location = Location.query.get(node.loc_id)
            location.lat = form.location.lat.data
            location.lon = form.location.lon.data
            node.location = location
            node.leader_id = form.leader.data
            db.session.commit()  # @UndefinedVariable
            flash("Node has beeen updated")
            
        # after creating the new state, redirect them back to dce config page
        return redirect(url_for("nodePage"))    
    return render_template("nodeForm.html", form=form)

# Obstacle Add/Edit Page
@app.route('/obstacles/add', defaults={'oid': None}, methods=['GET', 'POST'])
@app.route('/obstacles/<int:oid>/edit', methods=['GET', 'POST'])
def addEditObstacle(oid):
    obstacle = None
    form = ObstacleForm()  
    if oid is not None:
        obstacle = Obstacle.query.get(oid)
        
    if request.method == 'GET':
        if obstacle is None:
            form.new.data = True
        else:  
            form.new.data = False    
            form.id.data = obstacle.id
            form.location.lat.data = obstacle.location.lat
            form.location.lon.data = obstacle.location.lon    
    if request.method == 'POST' and form.validate():  # @UndefinedVariable
        if obstacle is None:
            #new obstacle has passed validation, add to db
            location = Location(lat=form.location.lat.data, lon=form.location.lon.data)
            db.session.add(location)  # @UndefinedVariable
            obstacle= Obstacle(location=location)
            db.session.add(obstacle)  # @UndefinedVariable
            db.session.commit()  # @UndefinedVariable
            flash("Obstacle has been created")
        else: 
            #node has been updated. save updates
            location = Location.query.get(obstacle.loc_id)
            location.lat = form.location.lat.data
            location.lon = form.location.lon.data
            db.session.commit()  # @UndefinedVariable
            flash("Obstacle has been updated")
        
        # after creating the new state, redirect them back to dce config page
        return redirect(url_for("obstaclePage"))    
    return render_template("obstacleForm.html", form=form)

'''
# Path Add/Edit Page
@app.route('/path/add', defaults={'path_id': None}, methods=['GET', 'POST'])
@app.route('/path/<int:path_id>/edit', methods=['GET', 'POST'])
def addEditPath(path_id):
    path = None
      
    # get choices for node leaders
    node_choices = [(0, 'Self')]
    for x in Node.query.filter_by(leader_id=0):   # @UndefinedVariable
        node_choices.append((x.id,x.name))
    form = PathForm()
    form.node.choices = node_choices
    form.node.default = 0   
    if path_id is not None:
        path = Path.query.get(path_id)
        
    if request.method == 'GET':
        if path is None:
            form.new.data = True
        else:  
            form.new.data = False    
            form.id.data = path.id
            form.node.data = path.nid  
            points = []
            for point in path.points:
                form.points.append_entry({"pid": point.id, "lat": point.location.lat, "lon":point.location.lon })  
            #form.points.add_entry()
    if request.method == 'POST' and form.validate():  # @UndefinedVariable
        if path is None:
            # path has been created.
            path = Path()
            path.nid = form.node.data
            db.session.add(path)
            db.session.commit()            
            for index, point in enumerate(form.points.data):
                newPoint = PathPoint()
                newPoint.path_id = path.id
                
                location = Location(lat=point['lat'], lon=point['lon'])
                db.session.add(location)  # @UndefinedVariable
                
                newPoint.location = location
                newPoint.position = int(point['pos']) + 1
                
                db.session.add(newPoint)
            db.session.commit()
            flash("Path has beeen created")
        else: 
            # path has been created.
            path.nid = form.node.data 
            
            # create a list of all points already included on this path. will be used to determine if
            # any points were deleted from the list.
            deleteList = [] 
            for point in path.points:
                deleteList.append(point.id)
            for index, point in enumerate(form.points.data):
                if int(point['pid']) == 0:
                    
                    newPoint = PathPoint()
                    newPoint.path_id = path.id
                
                    location = Location(lat=point['lat'], lon=point['lon'])
                    db.session.add(location)  # @UndefinedVariable
                
                    newPoint.location = location
                    newPoint.position = int(point['pos']) + 1
                
                    db.session.add(newPoint)
                else: 
                    # found existing point. update and remove from delete list
                    savedPoint = PathPoint.query.get(point['pid'])
                    savedPoint.position = int(point['pos']) + 1
                    savedLoc = Location.query.get(savedPoint.loc_id)
                    savedLoc.lat = point['lat']
                    savedLoc.lon = point['lon']
            
                    deleteList.remove(int(point['pid']))
                    
            for pid in deleteList:
                point = PathPoint.query.get(pid)
                db.session.delete(point)
            
            db.session.commit()                    
            flash("Path has beeen updated")
        
        # after creating the new state, redirect them back to dce config page
        return redirect(url_for("pathPage"))    
    elif request.method == 'POST' and not form.validate():
        flash_errors(form)
    return render_template("pathForm.html", form=form)
'''

# Node View page
@app.route('/node')
def nodePage():    
    nodes = Node.query.all()    # @UndefinedVariable   
    return render_template('nodes.html', nodes=nodes)

# Obstacle View page
@app.route('/obstacles')
def obstaclePage():    
    obstacles = Obstacle.query.all()    # @UndefinedVariable   
    return render_template('obstacles.html', obstacles=obstacles)

#####################################################################
###                      Helper Functions                         ###
#####################################################################

class ChartPoint(object):
    nid = 0
    lid = 0
    path = 0
    pid = 0
    x = 0
    y = 0
    color = ""
    name = ""
    marker = ""
    size=6
     
    def __init__(self, x, y, color=None, name=None, symbol=None, nid=None, lid=None, path=None, pid=None, size=None):
        self.x = x
        self.y = y
        if nid is not None:
            self.nid = nid
        if lid is not None:
            self.lid = lid
        if pid is not None:
            self.pid = pid
        if path is not None:
            self.path = path
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

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

def multikeysort(items, columns):
    from operator import itemgetter
    comparers = [((itemgetter(col[1:].strip()), -1) if col.startswith('-') else
                  (itemgetter(col.strip()), 1)) for col in columns]
    def comparer(left, right):
        for fn, mult in comparers:
            result = cmp(fn(left), fn(right))
            if result:
                return mult * result
        else:
            return 0
    return sorted(items, cmp=comparer)
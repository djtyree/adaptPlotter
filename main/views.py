from flask import render_template, jsonify, request, flash, redirect, url_for, json, Response
from main import app, db, subscriptions
from models import Node, Location, Obstacle, JumpPoint, Goal
from forms import NodeForm, ObstacleForm
import random
from gevent.queue import Queue

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
    leaders = Node.query.filter_by(leader_id=0).all() #  @UndefinedVariable
    
    map_n = { 'name': 'Node', 'color': '#AAAAAA', 'data': [], 'marker': {'symbol': 'triangle', 'radius': 6}, 'zIndex': 3 } 
    map_jp = { 'lineWidth': 1,'name': 'Jump Points', 'color': '#FF0000', 'data': [], 'marker': {'symbol': 'square', 'radius': 2}, 'zIndex': 1 }
    map_o = { 'name': 'Obstacles', 'color': '#00FF00', 'data': [], 'marker': {'symbol': 'circle', 'radius': 3}, 'zIndex': 2 }
    map_g = { 'name': 'Goals', 'color': '#0000FF', 'data': [], 'marker': {'symbol': 'square', 'radius': 6}, 'zIndex': 2 }
    
    for leader in leaders:
        map_n['data'].append(ChartPoint(x=leader.location.lon,
                                        y=leader.location.lat,
                                        color='#0000FF', 
                                        name=leader.name,
                                        nid=leader.id, 
                                        dir=leader.location.dir, 
                                        speed=leader.location.speed, 
                                        fdir=leader.force_dir, 
                                        fspeed=leader.force_speed, 
                                        size=8
                                    ).__dict__)
        map_jp['data'].append(ChartPoint(x=leader.location.lon,y=leader.location.lat, name='-', node=leader.id).__dict__)
        for jp in leader.jumppoints:
            map_jp['data'].append(ChartPoint(x=jp.location.lon,y=jp.location.lat, name='Jump Point - ' + str(jp.id),id=jp.id, node=leader.id).__dict__)
        for goal in leader.goals:
            map_g['data'].append(ChartPoint(x=goal.location.lon,y=goal.location.lat, name='Goal - ' + str(goal.id),id=goal.id, node=leader.id).__dict__)
        for follower in leader.followers:
            map_n['data'].append(ChartPoint(x=follower.location.lon,y=follower.location.lat, name=follower.name,nid=follower.id,lid=leader.id).__dict__)
    for obj in obstacles:
        map_o['data'].append(ChartPoint(x=obj.location.lon,y=obj.location.lat,name='Point - ' + str(obj.id)).__dict__)

    data = [map_n, map_jp, map_o, map_g]
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
        node = Node.query.get(node_id)  # @UndefinedVariable
        
    if request.method == 'GET':
        if node is None:
            form.new.data = True
        else:
            form.new.data = False
            form.id.data = node.id
            form.name.data = node.name
            form.rid.data = node.rid
            form.location.lat.data = node.location.lat
            form.location.lon.data = node.location.lon
            form.leader.data = node.leader_id    
 
            jumppoints = []
            for jp in node.jumppoints:
                form.jumppoints.append_entry({"jp_id": jp.id, "lat": jp.location.lat, "lon":jp.location.lon })
            goals = []
            for goal in node.goals:
                form.goals.append_entry({"goal_id": goal.id, "lat": goal.location.lat, "lon":goal.location.lon })  
    elif request.method == 'POST' and form.validate():  # @UndefinedVariable
        if node is None:
            #new node has passed validation, add to db
            location = Location(lat=form.location.lat.data, lon=form.location.lon.data)
            db.session.add(location)  # @UndefinedVariable
            node = Node(name=form.name.data, leader_id=form.leader.data, location=location, rid=form.rid.data)
            db.session.add(node)  # @UndefinedVariable
            db.session.commit()  # @UndefinedVariable
            
            for index, point in enumerate(form.jumppoints.data):
                jp = JumpPoint()
                
                location = Location(lat=point['lat'], lon=point['lon'])
                db.session.add(location)  # @UndefinedVariable
                
                jp.location = location
                jp.position = int(point['pos']) + 1
                
                db.session.add(jp)
                node.jumppoints.append(jp)
            
            for index, point in enumerate(form.goals.data):
                goal = Goal()
                
                location = Location(lat=point['lat'], lon=point['lon'])
                db.session.add(location)  # @UndefinedVariable
                
                goal.location = location
                goal.position = int(point['pos']) + 1
                
                db.session.add(goal)
                node.goals.append(goal)
                
            db.session.commit()  # @UndefinedVariable
            flash("Node has been created")
        else: 
            #node has been updated. save updates
            node.name = form.name.data
            node.rid = form.rid.data
            location = Location.query.get(node.loc_id)  # @UndefinedVariable
            location.lat = form.location.lat.data
            location.lon = form.location.lon.data
            node.location = location
            node.leader_id = form.leader.data

            # create a list of all points already included on this path. will be used to determine if
            # any points were deleted from the list.
            deleteList = [] 
            for jp in node.jumppoints:
                deleteList.append(jp.id)
            for index, jp in enumerate(form.jumppoints.data):
                if int(jp['jp_id']) == 0:
                    
                    newjp = JumpPoint()
                
                    location = Location(lat=jp['lat'], lon=jp['lon'])
                    db.session.add(location)  # @UndefinedVariable
                
                    newjp.location = location
                    newjp.position = int(jp['pos']) + 1            
                    db.session.add(newjp)
                    node.jumppoints.append(newjp)
                else: 
                    # found existing point. update and remove from delete list
                    savedjp = JumpPoint.query.get(jp['jp_id'])   # @UndefinedVariable
                    savedjp.position = int(jp['pos']) + 1
                    savedLoc = Location.query.get(savedjp.loc_id)   # @UndefinedVariable
                    savedLoc.lat = jp['lat']
                    savedLoc.lon = jp['lon']
            
                    deleteList.remove(int(jp['jp_id']))
                    
            for id in deleteList:
                jp= JumpPoint.query.get(id)  # @UndefinedVariable
                db.session.delete(jp)
            
            deleteList = [] 
            for goal in node.goals:
                deleteList.append(goal.id)
            for index, goal in enumerate(form.goals.data):
                if int(goal['goal_id']) == 0:
                    
                    newgoal = Goal()
                
                    location = Location(lat=goal['lat'], lon=goal['lon'])
                    db.session.add(location)  # @UndefinedVariable
                
                    newgoal.location = location
                    newgoal.position = int(goal['pos']) + 1            
                    db.session.add(newgoal)
                    node.jumppoints.append(newgoal)
                else: 
                    # found existing point. update and remove from delete list
                    savedGoal = Goal.query.get(goal['goal_id'])   # @UndefinedVariable
                    savedGoal.position = int(goal['pos']) + 1
                    savedLoc = Location.query.get(savedGoal.loc_id)   # @UndefinedVariable
                    savedLoc.lat = goal['lat']
                    savedLoc.lon = goal['lon']
            
                    deleteList.remove(int(goal['goal_id']))
                    
            for id in deleteList:
                goal= Goal.query.get(id)  # @UndefinedVariable
                db.session.delete(goal)
            db.session.commit()                    
            flash("Node has been updated")
        
            
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
        obstacle = Obstacle.query.get(oid)  # @UndefinedVariable
        
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
            location = Location.query.get(obstacle.loc_id)  # @UndefinedVariable
            location.lat = form.location.lat.data
            location.lon = form.location.lon.data
            db.session.commit()  # @UndefinedVariable
            flash("Obstacle has been updated")
        
        # after creating the new state, redirect them back to dce config page
        return redirect(url_for("obstaclePage"))    
    return render_template("obstacleForm.html", form=form) 
    
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

# Delete Data
@app.route('/data/delete', methods=['POST'])
def deleteData():    
    id = str(request.json['data_id'])
    type = str(request.json['data_type'])
    
    msg = 'No message'
    if type =='node':
        node = Node.query.filter_by(id=id).first()  # @UndefinedVariable
        for follower in node.followers:
            follower.leader_id = 0
        db.session.delete(node) 
    elif type =='obstacle':
        if id== "all":
            obstacles = Obstacle.query.all()  # @UndefinedVariable
            for ob in obstacles:
                db.session.delete(ob)
        else:
            obstacle = Obstacle.query.filter_by(id=id).first()  # @UndefinedVariable
            db.session.delete(obstacle)
        msg = "Obstacle has been deleted."
    else:
        return jsonify({'status': "ERROR", 'msg':'Data type was not present or unrecognized '})
    db.session.commit()  # @UndefinedVariable
    return jsonify({'status':'OK','msg': msg})
    
# Delete Data
@app.route('/data/addGoal', methods=['POST'])
def addGoal():
    lid = str(request.json['leader'])    
    lat = str(request.json['lat'])
    lon = str(request.json['lon'])
    
    msg = 'No message'
    
    if int(lid) == 0:
        # no leader specified, grab first leader in db
        leader = Node.query.filter_by(leader_id=0).first()  # @UndefinedVariable
        goal = Goal()
        location = Location(lat=lat, lon=lon)
        db.session.add(location)  # @UndefinedVariable
        
        goal.location = location
        goal.position = len(leader.jumppoints) + 1
        
        db.session.add(goal)
        leader.goals.append(goal)
        db.session.commit()
        return jsonify({'status':'OK','msg': "Goal Added"})    
    
    return jsonify({'status':'ERRROR','msg': msg})

class ServerSentEvent(object):
    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "adapt_update",
            self.id : "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k) 
                 for k, v in self.desc_map.iteritems() if k]
        
        return "%s\n\n" % "\n"  .join(lines)
    
@app.route('/get_subs')
def getSubs():
    return "Currently %d subscriptions" % len(subscriptions)
    
@app.route('/sse_event_source')
def sse_request():
    def gen():
        global subscriptions
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")

#####################################################################
###                      Helper Functions                         ###
#####################################################################

class ChartPoint(object):
    nid = 0
    lid = 0
    node = 0
    id = 0
    x = 0
    y = 0
    color = ""
    name = ""
    marker = ""
    size=6
    speed=0.0
    dir=0.0
    fspeed=0.0
    fdir=0.0
     
    def __init__(self, x, y, color=None, name=None, symbol=None, nid=None, lid=None, node=None, id=None, size=None, speed=None, dir=None, fspeed=None, fdir=None):
        self.x = x
        self.y = y
        if nid is not None:
            self.nid = nid
        if lid is not None:
            self.lid = lid
        if id is not None:
            self.id = id
        if node is not None:
            self.node = node
        if color is not None:
            self.color = color
        if name is not None:
            self.name = name
        if dir is not None:
            self.dir = dir
        if speed is not None:
            self.speed = speed
        if fdir is not None:
            self.fdir = fdir
        if fspeed is not None:
            self.fspeed = fspeed
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

def publish_events(reqType=None, rid=0):
    global subscriptions
    if rid==0:
        print "No robot id"
        return
    def notify():
        data = None
        msg = ""
        if len(subscriptions):
            if reqType=="nodeLocation":
                print "Node id=" + str(rid)
                node = Node.query.get(rid)    # @UndefinedVariable
                #node = Node.query.get(id)
                #msg = json.dumps(dict(nid=node.id, rid=node.rid, lat=node.location.lat, lon=node.location.lon))                
                msg =  json.dumps(dict(type=reqType, nid=node.id, rid=node.rid, lat=node.location.lat, lon=node.location.lon))  
            if msg is not "":
                #msg = json.dumps(dict(run=run.id, dce=dce.id, state=state.id, state_name=state.name, start_time=run.start_time))
                for sub in subscriptions[:]:
                    sub.put(msg)
    notify()  
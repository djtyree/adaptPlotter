from flask import render_template, jsonify
from main import app, db
from models import Object, Node
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
    
    nodes = []
    paths = []
    points = []
    
    return jsonify({'status':'OK','data':data})

# New State Page
@app.route('/node/add', methods=['GET', 'POST'])
def newNodePage():    
    form = NodeForm(new=True)
    leader_choices = [(0, 'Self')]
    for x in Node.query.all():   # @UndefinedVariable
        leader_choices.append((x.id,x.name))
    form.leader.choices = leader_choices
    form.leader.default = 0
    
    file_choices = []
    for x in BlackoutFile.query.all():   # @UndefinedVariable
        file_choices.append((x.id,x.name))
    form.blackoutfile.choices = file_choices
    
    if request.method == 'POST' and form.validate():  # @UndefinedVariable
        #new run has passed validation, add to db
        run = Run(scheduled_start=form.start.data, blackout_id=form.blackoutfile.data)
        if form.courses.data is not 0:
            # hardcoded state with id=1 to be default state
            run.course_id = form.courses.data
           
            course = Course.query.get(run.course_id)
            
            if course.dce_id is None:
                flash("No DCE assigned to this course", 'error')
            
            #check if there is a run for the selected course within an hour of another run's scheduled start or actual start time
            same_run = Run.query.filter(Run.course_id==form.courses.data,( Run.scheduled_start>=int(form.start.data)-3600) | (Run.start_time>=int(time.time()-3600))).first()
            if same_run is not None:
                flash("A run already exists within 1 hour for course " + str(form.courses.data) + ". Verify the course and start time for the created run", 'error')
                
            db.session.add(run)  # @UndefinedVariable
            db.session.commit()  # @UndefinedVariable
            flash("Run has beeen created")
            
        # after creating the new state, redirect them back to dce config page
        return redirect(url_for("run.runPage"))    
    return render_template("run/runForm.html", form=form)
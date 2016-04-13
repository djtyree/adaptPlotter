<h1 style="text-align: center">DCE Web</h1>


| Requirement | Description | Install  |
| ------------| ------------| ------------ | 
| Python      | Application Language | http://docs.python-guide.org/en/latest/ |  
| Pip         | Python Package Installer | https://pip.pypa.io/en/latest/installing.html |
| PyGal	      | Python Charts Generator | sudo pip install pygal |
| GEvent             | coroutine-based Python networking library that uses greenlet to provide a synchronous API | sudo pip install GEvent |
| Flask	      | Python micro webdevelopment framework | sudo pip install Flask |
| Flask-Login	      | Flask extension to assist w/ user login | sudo pip install Flask-Login |
| Flask-SQLALchemy	      | Flask extension to assist w/ db management | sudo pip install Flask-SQLAlchemy |
| Flask-Migrate	      | Flask extension to assist w/ db administration | sudo pip install Flask-Migrate |
| FLask-Script        | Flask extension used to add runtime arguments | sudo pip install Flask-Script |
| Flask-WTF           | Flask extension used to assist in form building | sudo pip install Flask-WTF |
| Flask-Moment           | Flask extension used to assist in dates | sudo pip install Flask-Moment |
| Flask-RESTful           | Flask extension used to implement a REST API | sudo pip install Flask-RESTful |
| Flask-HttpAuth           | Flask extension used to implement authentication for rest server | sudo pip install Flask-HttpAuth |
| Flask-Widgets           | Another Flask extension used to assist in form building | sudo pip install Flask-Widgets |
| Flask-BCRYPT           | Flask extension used to assist login | sudo pip install Flask-Bcrypt |
| Flask-Uploads           | Flask extension used to assist file uploads | sudo pip install Flask-Uploads |
  

<h3>Requirments Install</h3>
* After installing Python and PIP.
	 * pip install -r requirements.txt
	 * If this fails, you can manually install from the list above
	 
<h3>Eclipse IDE Setup</h3>
1. Help -> Install New Software...
2. http://pydev.org/updates
     * This will install python support to eclipse
3. Eclipse -> Preferences...
4. Pydev -> Interpreters -> PyDev Interpreters -> Forced Builtins...
5. New...
     * flask.ext
     * flaskext

<h3>Creation of Run Configurations</h3>
1. Right click on main package ('dceweb')
2. Run As -> Run Configurations ...
3. Right click on python run -> New
4. Create the following configurations
	* Name: **Main**
      * Project: dceweb
      * Main Module: ${workspace_loc:dceweb/runserver.py}
      * Program Arguments: runserver
      * Working Directory: ${workspace_loc:dceweb}
    * Name: **DB Init**
      * Project: dceweb
      * Main Module: ${workspace_loc:dceweb/runserver.py}
      * Program Arguments: db init
      * Working Directory: ${workspace_loc:dceweb}
    * Name: **DB Migrate**
      * Project: dceweb
      * Main Module: ${workspace_loc:dceweb/runserver.py}
      * Program Arguments: db migrate
      * Working Directory: ${workspace_loc:dceweb}
    * Name: **DB Upgrade**
      * Project: dceweb
      * Main Module: ${workspace_loc:dceweb/runserver.py}
      * Program Arguments: db upgrade
      * Working Directory: ${workspace_loc:dceweb}
  
<h3>Running the Server</h3>
1. Initial Db Creation
	* Run the DB Init configuration
2. Any modifications needed such as new tables or schema changes
    *  Run the DB Migrate configuration
    *  Run the DB Upgrade configuration
3. Starting the Twisted Server
    * Run the Main configuration
        
    

#!flask/bin/python
from main import app, manager
import config

@manager.command
def runserver():
    print "Kicking off the server on localhost: " + str(config.PORT)
    app.run(debug=config.DEBUG)

if __name__ == '__main__':
    manager.run()
    
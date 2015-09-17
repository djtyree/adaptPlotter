#!flask/bin/python
from gevent.wsgi import WSGIServer
from main import app, manager
import config

@manager.command
def runserver():
    print "Kicking off the server on localhost: " + str(config.PORT)
    #app.run(host='0.0.0.0', debug=config.DEBUG)
    server = WSGIServer(("", 5000), app)
    server.serve_forever()
    
if __name__ == '__main__':
    manager.run()
    
    
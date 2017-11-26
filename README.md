<p align="center">
  <img src="https://github.com/tarelli/bucket/blob/master/geppetto%20logo.png?raw=true" alt="Geppetto logo"/>
</p>

# Geppetto Tornado-Flask Template
Geppetto Tornado-Flask Template provides a template to develop a Geppetto Instance in Python. This Tornado-Flask application provides the minimum infrastructure to start a simple Geppetto Instances and illustrates how to extend and customize Geppetto server side.

This template provides a very basic python infrastructure to serve the static content. The static content (JS + HTML) can be found at org.geppetto.frontend (https://github.com/openworm/org.geppetto.frontend) and the same module is reused for the Geppetto Java Version. Note, however, that the python server implementation is a work in progress and some features have not been migrated from Java yet.

This skeleton app has been developed combining Flask and Tornado. Flask servers the webpages/REST api while Tornado handles the websocket connections for us. This way we leverage both the excellent asynchronous features of Tornado and the power and ease of use of Flask through Tornado's. Gettting the simplicity of Flask with the async performance of Tornado.

## Installation

**Dependencies**
```
pip install flask
pip install flask-restful
pip install tornado
```

**Install Tornado-Flask Template**

```
git clone https://github.com/MetaCell/geppetto-tornado-flask-template
cd geppetto-tornado-flask-template
git clone https://github.com/openworm/org.geppetto.frontend
cd org.geppetto.frontend/src/main/webapp
npm install
npm run build-dev-noTest
```

## Start the server
```
python pygeppetto_template.py
```

Go to http://localhost:5000/ and enjoy!

## How to develop

In order to get your python changes redeployed you will have to restart the python server. To implement an automatically redeploy server should be straight-forward but it has not been implemented as part of this skeleton app.

JS/HTML code can be found inside `/org.geppetto.frontend/src/main/webapp/`. The code needs to be rebuilt with webpack everytime there is a change. The recommended way is to run in `/org.geppetto.frontend/src/main/webapp/` this command:
```
npm run build-dev-noTest:watch
```
## Features

**Serve main Geppetto webpage and Geppetto API**

Flask is in charge of the web pages and templates handling. In order to provide a modularised interface this code has been implemented using [Blueprint](http://flask.pocoo.org/docs/0.12/blueprints/)

Geppetto specific code should go inside pygeppetto_blueprint.py and extend the current pygeppetto_core. At the moment it just renders the template whenever there is a request to Geppetto.

pygeppetto_core (core blueprint) can (and should) be extended from the actual application. In this skeleton, we are reusing this blueprint withint pygeppetto_template.
```
app = Flask(__name__)
app.register_blueprint(pygeppetto_core, url_prefix='/')
```

**Implement Websocket communication**

Websockets are implemented using the powerful Tornado infrastructure. Implementation can be found at pygeppetto_server.py as part of the WebSocket class.

Two methods are implemented so far:
- ws_connect
- ws_receive

Currently, three request are sort of handle:
- client_id (on connection)
- user_priveleges (on connection)
- geppetto_version (on message)

This is enought to load a basic geppetto canvas (geppetto.vm template).

Mapping (Controller) between url and python class is defined in the run method of pygeppetto_server.py
```
server = Application([
        (r'/org.geppetto.frontend/GeppettoServlet', WebSocket),
        ...
    ], debug=True)
```

**Initialise Tornado server**

Initialization of the tornado server happens as part of the PyGeppettoServer class inside pygeppetto_server.py. This is the main code:
```
container = WSGIContainer(self.app)
server = Application([
    (r'/org.geppetto.frontend/GeppettoServlet', WebSocket),
    (r'/org.geppetto.frontend/geppetto/(.*)', StaticFileHandler, {'path': 'org.geppetto.frontend/src/main/webapp/'}),
    (r'.*', FallbackHandler, dict(fallback=container))
], debug=True)
server.listen(port)
IOLoop.instance().start()
```

Apart from starting the Tornado application and route the main socket communication it defines two other handlers. A static handler for all the static content inside org.geppetto.frontend and a fallback handler to Flask. Any unknown request will be forward to Flask side which will take care of it.

**Extend API**

An example of a very simple REST API is provided together with this skeleton. You will find it inside pygeppetto_template.

Basically using the flask_restful api we extend the app to handle GET and POST request to `/api/people`.

```
api.add_resource(People, '/api/people')
```

Any request at this end point will be handled by the People class.

**What is missing?**

- Implement hot deploy for the python code. [This library](http://werkzeug.pocoo.org) offers a good set of WSGI utilities in python. In particular [this debugger](http://werkzeug.pocoo.org/docs/0.12/debug/) utility may be useful.

- This skeleton app is not connected to any database but, as it is implemented on top of the Trnado server, it should be quite simple to integrate any SQL DB.

- Extract the main core features into another python package. This package will contain the basic functionality (sockets + template redirection). An example of this sort of modules has been implemented [here](https://github.com/MetaCell/pygeppetto-django) for Django.


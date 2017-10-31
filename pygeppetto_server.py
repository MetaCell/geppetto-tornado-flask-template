import json
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler
from tornado.ioloop import IOLoop


class WebSocket(WebSocketHandler):
    def open(self):
        print("Socket opened.")
        # 1 -> Send the connection
        self.write_message(
            {"type": "client_id", "data": "{\"clientID\":\"Connection1\"}"})
        # 2 -> Check user privileges
        self.write_message(
            {"type": "user_privileges", "data": "{\"user_privileges\": \"{\\\"userName\\\":\\\"Python User\\\",\\\"loggedIn\\\":true,\\\"hasPersistence\\\":false,\\\"privileges\\\":[\\\"READ_PROJECT\\\",\\\"DOWNLOAD\\\",\\\"DROPBOX_INTEGRATION\\\", \\\"RUN_EXPERIMENT\\\", \\\"WRITE_PROJECT\\\"]}\"}"})

    def on_message(self, message):
        print("Geppetto Version 0.3.7")
        jsonMessage = json.loads(message)
        if (jsonMessage['type'] == 'geppetto_version'):
            # Where do we get the geppetto version from?
            self.write_message({"requestID": jsonMessage[
                               'requestID'], "type": "geppetto_version", "data": "{\"geppetto_version\":\"0.3.7\"}"})

    def on_close(self):
        print("Socket closed.")

class PyGeppettoServer():
    def __init__(self, app=None):
        self.app = app

    def sockets(self, handlers):
        self.socket_handlers = handlers

    def run(self, port=5000, host='127.0.0.1', **kwargs):
        container = WSGIContainer(self.app)
        server = Application([
            (r'/org.geppetto.frontend/GeppettoServlet', WebSocket),
            (r'/org.geppetto.frontend/geppetto/(.*)', StaticFileHandler, {'path': 'org.geppetto.frontend/src/main/webapp/'}),
            (r'.*', FallbackHandler, dict(fallback=container))
        ], debug=True)
        server.listen(port)
        IOLoop.instance().start()


# from . import Server, Client
from flask import Flask 
from flask_socketio import SocketIO

application = Flask(__name__)
socket_app = SocketIO(application)

@socket_app.on("message")
def handle_message(message):
    print("received a message: " + message)

if __name__ == "__main__":
    socket_app.run(application, host = '192.168.1.27', debug = True)
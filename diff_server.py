# from . import Server, Client
from flask import Flask, request
from flask_socketio import SocketIO, send, emit

import diff_match_patch as dmp

import json

import threading
import time

application = Flask(__name__)
socket_app = SocketIO(application)

server_shadows = {}
cursor_positions = {}
names = {}
server_text = ""
patcher = dmp.diff_match_patch()

def ack():
    print("received")

@socket_app.on("message")
def handle_message(message):
    print("received a message: " + message)

@socket_app.on("connect")
def handle_connect():
    print("Connected to session ", request.sid)
     
@socket_app.on("connect-response")
def handle_connect_response(user):
    # TODO: Obviously some kind of authentication would happen here

    name = user['id']

    print("\n\n\n" + name + "\n\n\n")

    if name not in names: 
        names[name] = request.sid

    else:
        # replace the old sid
        sid = names[name]

        del server_shadows[sid]
        del cursor_positions[sid]

        names[name] = request.sid
    
    server_shadows[request.sid] = server_text
    send(server_text)

@socket_app.on("sync")
def sync(patches):
    global server_text

    print("\nDocument was changed, here are the patches: " + patches['patches'] + "\n")

    cursor_positions[request.sid] = [patches['row'], patches['column']]

    emit("sync", {"patches" : "", "cursor_positions" : json.dumps(cursor_positions)}, callback = ack)

    patches = patcher.patch_fromText(patches['patches'])

    # apply patches
    server_shadows[request.sid] = patcher.patch_apply(patches, server_shadows[request.sid])[0] 
    server_text, r = patcher.patch_apply(patches, server_text)

    print("SERVER TEXT: " + server_text + str(r))

def start_server():
    print('Starting server')
    socket_app.run(application, host = '192.168.1.11', debug = True)

def synchronization():
    print("Starting synchronization loop")
    
    c = 0
    while True:
        c += 1

        unsynced = False
        for sid in server_shadows:
            if server_shadows[sid] != server_text:
                unsynced = True 

                patches = patcher.patch_make(server_shadows[sid], server_text)

                server_shadows[sid] = server_text 

                socket_app.emit("sync", {"patches" : patcher.patch_toText(patches), "cursor_positions" : json.dumps(cursor_positions)}, room = sid, callback = ack)
        
        if (not unsynced):
            print("Reached equilibrium")

        time.sleep(0.5)

        if c % 100 == 0:
            print("Running for " + str(c * 0.5) + " seconds")

if __name__ == "__main__":
    sync_loop = threading.Thread(target = synchronization)

    sync_loop.start()

    start_server()
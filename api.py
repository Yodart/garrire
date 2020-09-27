from flask import Flask, jsonify
from users import users
from auth import auth
from rooms import rooms
from flask_socketio import SocketIO, join_room
from db import db_connect
import os
import sys

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)
app.register_blueprint(auth)
app.register_blueprint(users)
app.register_blueprint(rooms)


@socketio.on('join')
def join(data):
    join_room(data['room'])
    socketio.emit("join", data)


@socketio.on('message')
@db_connect
def message(db_cursor, db_connection, data):
    print(data['room'])
    db_cursor.execute(
        "INSERT INTO messages (username,content,room) values(%s,%s,%s)", (data['username'], data['message'], data['room']))
    db_connection.commit()
    socketio.emit("message", data, room=data['room'])
    db_cursor.close()
    db_connection.close()


if __name__ == '__main__':
    socketio.run(app, debug=True)

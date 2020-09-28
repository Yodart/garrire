from flask import Flask, jsonify,request
from users import users
from auth import auth
from rooms import rooms
from flask_socketio import SocketIO, join_room
from db import db_connect
import os
import sys
import pika

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)
app.register_blueprint(auth)
app.register_blueprint(users)
app.register_blueprint(rooms)

@app.route('/message', methods=['POST'])
@db_connect
def message(db_cursor, db_connection):
    try:
        data = request.json
        if data['secret']=='jobsitystockbotkey':
            db_cursor.execute(
                "INSERT INTO messages (username,content,room) values(%s,%s,%s)", (data['username'], data['message'], data['room']))
            db_connection.commit()
            socketio.emit("message", data, room=data['room'])
            db_cursor.close()
            db_connection.close()
            return {'response': 'Message sent'},200
        return{'response': 'Insufficient permissions'}, 401
    except:
        return {'response': 'Unable to send message. Insufficient or wrong data provided'},401

@socketio.on('join')
def join(data):
    join_room(data['room'])
    socketio.emit("join", data)

@socketio.on('message')
@db_connect
def message(db_cursor, db_connection, data):
    db_cursor.execute(
        "INSERT INTO messages (username,content,room) values(%s,%s,%s)", (data['username'], data['message'], data['room']))
    db_connection.commit()
    socketio.emit("message", data, room=data['room'])
    db_cursor.close()
    db_connection.close()
    message = data['message']
    if message.startswith('/stock=') and len(message)>7:
        try:
            stock = message.replace('/stock=','')
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='stock-query')
            channel.basic_publish(exchange='',routing_key='stock-query',body="{}|{}".format(stock,data['room']))
            connection.close()
        except:
            print(str(sys.exc_info()))


if __name__ == '__main__':
    socketio.run(app, debug=True)

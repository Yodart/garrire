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


# Endpoint to be consumed by the StockBot to publish messages to a direct room
# it uses a secretkey to ensure security and after checking for that it emmits 
# the socket io message to be rendered on the client side.

@app.route('/message', methods=['POST'])
@db_connect
def message(db_cursor, db_connection):
    try:
        data = request.json
        if data['secret']=='jobsitystockbotkey':
            socketio.emit("message", data, room=data['room'])
            return {'response': 'Message sent'},200
        return{'response': 'Insufficient permissions'}, 401
    except:
        return {'response': 'Unable to send message. Insufficient or wrong data provided'},401


# SocketIO callback for when a user joins a room it basically just emmits an
# announcement that will be consumed on the client side.

@socketio.on('join')
def join(data):
    join_room(data['room'])
    socketio.emit("join", data)


# SocketIO callback for when a the client sends a message in a chat room. It stores
# that message record on the database and then emits back a message to the client that
# will there be consumed and rendered. Finally it checks if the message has the bot
# message format and if so adds that job onto the bot RabbitMQ queu that will be consumed
# and ultimately processed by the bot to post a message on the channel.

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

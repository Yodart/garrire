from flask import Flask, Blueprint, request, jsonify, make_response, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connect
from auth import require_auth_token
import datetime
import jwt
import psycopg2
import sys

rooms = Blueprint('rooms', __name__)

# Endpoint to see all the available room. It checks if the current user
# is logged in and if so it renders the UI for that user to pick a room
# to join and start chatting.

@ rooms.route('/rooms', methods=['GET'])
@db_connect
@require_auth_token
def rooms_list(current_user, db_cursor, db_connection):
    if request.method == "GET":
        db_cursor.execute("SELECT id,name,created FROM rooms")
        rooms = []
        for room in db_cursor.fetchall():
            rooms.append({'id': room[0],
                          'name': room[1],
                          'created': room[2]})
        return render_template("/rooms/rooms.html", username=current_user['username'], rooms=rooms)


# Endpoint to enter a room. It takes the room name from the path, check
# if the current user is logged in an if so displays the chat interface
# after fetching the last 50 messages on that room.

@ rooms.route('/rooms/<string:room>', methods=['GET'])
@db_connect
@require_auth_token
def room(current_user, db_cursor, db_connection, room):
    if request.method == "GET":
        db_cursor.execute(
            "SELECT username,content,timestamp FROM messages WHERE room=%s LIMIT 50", ([room]))
        messages = []
        for message in db_cursor.fetchall():
            messages.append({'username': message[0],
                             'message': message[1],
                             'timestamp': message[2]})
        return render_template("/rooms/chat.html", username=current_user['username'], room=room, messages=messages)

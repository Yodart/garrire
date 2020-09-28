from flask import Flask, Blueprint, request, jsonify, make_response, render_template, redirect,url_for 
from werkzeug.security import generate_password_hash, check_password_hash
from db import db_connect
from auth import require_auth_token
import datetime
import jwt
import psycopg2
import sys

users = Blueprint('users', __name__)

# Endpoint to create a new account, it takes in a username and a password,
# checks if the username is available and if so uses sha256 to encrypt the
# the user password and creates the record on the database.

@ users.route('/signup', methods=['GET','POST'])
@db_connect
def create_user(db_cursor, db_connection):
    if request.method == "GET":
        return render_template("/signup/signup.html")
    hashed_password = generate_password_hash(
        request.form.get('password'), method='sha256')
    username = request.form.get('username')
    try:
        db_cursor.execute(
            "SELECT username FROM users WHERE username=%s", ([username]))
        user_data = db_cursor.fetchall()[0]
        return render_template("/signup/fail.html")
    except:
        try:
            db_cursor.execute(
                "INSERT INTO users (username,password) values(%s,%s)", (username, hashed_password))
            db_connection.commit()
            return redirect("http://45.56.96.56:5000/login")
        except:
            return render_template("/signup/fail.html"),401


# Endpoint to query a single user based on its username, it only returns the
# data if the currently logged user is query his own data, if so it returns
# all the relavent userdata stored on the database.

@ users.route('/users/<string:username>', methods=['GET'])
@db_connect
@require_auth_token
def query_single_user(current_user, db_cursor, db_connection, username):
    if current_user['username']==None or current_user['username'] != username:
        return jsonify({"error": "Sensity user data, please log into the account"}), 401
    try:
        db_cursor.execute(
            "SELECT id,username,joined FROM users WHERE username=%s", ([username]))
        user_data = db_cursor.fetchall()[0]
        return {'id': user_data[0],
                'username': user_data[1],
                'joined': user_data[2]}, 200
    except:
        return {'error': "Unable to fetch /user/<username>", "traceback": str(sys.exc_info())}, 401


# Endpoint to delete an user account, it checks if the logged user owns the 
# account it intents to delete and if so deletes that user record from the db.

@ users.route('/users/<string:username>', methods=['DELETE'])
@db_connect
@require_auth_token
def delete_user(current_user, db_cursor, db_connection, username):
    if current_user['username'] != username:
        return jsonify({"error": "Sensity user data, please log into the user"}), 401
    try:
        db_cursor.execute(
            "DELETE FROM users WHERE username = %s", ([username]))
        db_connection.commit()
        return {'response': 'User deleted'}, 200
    except:
        return {'error': "Unable to delete user", "traceback": str(sys.exc_info())}



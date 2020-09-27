from flask import Flask, Blueprint, session,request, jsonify, make_response, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db import db_connect
import datetime
import jwt
import sys

auth = Blueprint('auth', __name__)


def require_auth_token(f):
    @wraps(f)
    @db_connect
    def decorated(db_cursor, db_connection, *args, **kwargs):
        token = None
        user = None
        if 'token' in session:
            token = session['token']
        if not token:
            print(jsonify({'error': 'Missing auth token'}))
            return redirect("http://127.0.0.1:5000/login")
        try:
            data = jwt.decode(token, 'secret')
            db_cursor.execute(
                "SELECT username FROM users WHERE username=%s", ([data['username']]))
            user_data = db_cursor.fetchall()[0]
            user = {'username': user_data[0]}
        except:
            print(jsonify({'error': 'Invalid auth token. Please login to your account'}))
            return redirect("http://127.0.0.1:5000/login")
        return f(user, *args, **kwargs)
    return decorated


@auth.route('/login', methods=['GET','POST'])
@db_connect
def login(db_cursor, db_connection):
    if request.method == "GET":
        return render_template("/login/login.html")
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return render_template("/login/fail.html")
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    try:
        db_cursor.execute(
            "SELECT username,password  FROM users WHERE username=%s", ([username]))
        user_data = db_cursor.fetchall()[0]
        user = {'username': user_data[0],
                'password': user_data[1]}
        if check_password_hash(user['password'], password):
            token = jwt.encode(
                {'username': user['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)}, 'secret')
            session["token"] = token
            return redirect("http://127.0.0.1:5000/rooms")
        print(jsonify({'message': "Wrong Password"}))
        return render_template("/login/fail.html")
    except:
         print(jsonify({'error': "Unable to find user", "traceback": str(sys.exc_info())}))
         return render_template("/login/fail.html")

import sqlite3, json, re
from functools import wraps
from datetime import datetime, timedelta

from flask import Flask, g, jsonify, request, abort
from flask_cors import CORS

from models import *

import jwt

# CHANGE TO SPECIFIC PATH TO YOUR COMPUTER (change 'kyle' to your username)
DATABASE_PATH = "/home/kyle/csci430-problem2/server/database.db"

# configuration
DEBUG = True
DATABASE = DATABASE_PATH
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# used for encryption and session management
SECRET_KEY = 'bigbootyhoes'

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# connect to database
def connect_db():
    """Connects to the database."""
    rv = sqlite3.connect(app.config["DATABASE"])
    rv.row_factory = sqlite3.Row
    return rv

# create the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

# open database connection
def get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# close database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/upload', methods=('POST',))
def upload():
    response = {}
    data = request.get_json()
    email = data.get('creator_email')
    name = data.get('name')
    file = data.get('file')
    token = data.get('token')
    validate = User.decode_auth_token(token, app.config['SECRET_KEY'])
    if validate != email:
        return jsonify( { 'error' : validate })
    photo = Photo(name, file, email)
    db = SQLAlchemy()
    db.session.add(photo)
    db.session.commit()
    return jsonify("success")

@app.route('/getImages', methods=('POST', ))
def getImages():
    response = {}
    data = request.get_json()
    email = data.get('email')
    token = data.get('token')
    validate = User.decode_auth_token(token, app.config['SECRET_KEY'])
    if validate != email:
        return jsonify( { 'error' : validate })
    db = get_db()
    imgs_conn = db.execute("select * from photos where creator_email=:email",
            { "email": email })
    imgs = imgs_conn.fetchall()
    response_imgs = []
    for row in imgs:
        temp = {
            'name': row['name'], 
            'file': row['file'].decode("utf-8")
            }
        response_imgs.append(temp)


    response['imgs'] = response_imgs
    response['status'] = 'success'
    return response

@app.route('/register', methods=('POST',))
def register():
    response = {}
    data = request.get_json()
    user = User(**data)
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('dob')
    password = data.get('password')
    passRegex = ("^(?=.*[a-z])(?=." +
     "*[A-Z])(?=.*\\d)" +
     "(?=.*[-+_!@#$%^&*., ?]).+$")
    p = re.compile(passRegex)
    emailRegex = ('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$')
    e = re.compile(emailRegex)
    if (email == '' or not re.search(e, email)):
        return jsonify({ 'error' : "Please enter a valid email"})
    elif (first_name == ''):
        return jsonify({ 'error' : "Please enter a first name"})
    elif (last_name == ''):
        return jsonify({ 'error' : "Please enter a last name"})
    elif (dob == ''):
        return jsonify({ 'error' : "Please enter a valid date of birth."})
    elif (len(password) < 8):
        return jsonify({ 'error' : "password too short"})
    elif (not re.search(p, password)):
        return jsonify({ 'error' : "password must contain a number, lowercase, uppercase, and special char"})
    db = get_db()
    known_users = db.execute('select * from users where email=:email',
            { "email": email })
    num_users = known_users.fetchall()
    if (len(num_users) != 0):
    	response['error'] = "Email taken"
    	return jsonify(response)
    db = SQLAlchemy()
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    email = data.get('email')
    user = User.authenticate(**data)

    if not user:
        return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

    token = user.encode_auth_token(email, app.config['SECRET_KEY']).decode()
    response = {
        'token': token,
        'status': 'success',
        'first_name': user.first_name,
        'last_name': user.last_name,
        'dob': user.dob
    }
    return jsonify(response)

if __name__ == '__main__':
	from models import db
	db.init_app(app)
	app.run()
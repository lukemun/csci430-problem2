import sqlite3, json, re
from functools import wraps
from datetime import datetime, timedelta


from flask import Flask, g, jsonify, request, abort
from flask_cors import CORS

from models import *

import jwt

# configuration
DEBUG = True
DATABASE = "database.db"
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# used for encryption and session management
SECRET_KEY = 'bigbootyhoes'

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# THIS NEEDS TO BE SECURED
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
    username = data.get('creator_name')
    name = data.get('name')
    file = data.get('file')
    token = data.get('token')
    validate = User.decode_auth_token(token, app.config['SECRET_KEY'])
    if validate != username:
        return jsonify( { 'error' : validate })
    photo = Photo(name, file, username)
    db = SQLAlchemy()
    db.session.add(photo)
    db.session.commit()
    return jsonify("success")

@app.route('/getImages', methods=('POST', ))
def getImages():
    response = {}
    data = request.get_json()
    username = data.get('username')
    token = data.get('token')
    validate = User.decode_auth_token(token, app.config['SECRET_KEY'])
    if validate != username:
        return jsonify( { 'error' : validate })
    db = get_db()
    imgs_conn = db.execute('select * from photos where creator_name = ?', [username])
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
    username = data.get('username')
    password = data.get('password')
    regex = ("^(?=.*[a-z])(?=." +
     "*[A-Z])(?=.*\\d)" +
     "(?=.*[-+_!@#$%^&*., ?]).+$")
    p = re.compile(regex)
    if (len(password) < 8):
        return jsonify({ 'error' : "password too short"})
    elif (not re.search(p, password)):
        return jsonify({ 'error' : "password must contain a number, lowercase, uppercase, and special char"})
    db = get_db()
    known_users = db.execute('select * from users where username = ?', [username])
    print ('known', known_users)
    num_users = known_users.fetchall()
    print ("# user with that username ", len(num_users))
    if (len(num_users) != 0):
    	print ('here')
    	response['error'] = "Username taken"
    	return jsonify(response)
    db = SQLAlchemy()
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/login', methods=('POST',))
def login():
    data = request.get_json()
    username = data.get('username')
    user = User.authenticate(**data)

    if not user:
        return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

    token = user.encode_auth_token(username, app.config['SECRET_KEY'])
    # token = jwt.encode({
    #     'sub': user.username,
    #     'iat':datetime.utcnow(),
    #     'exp': datetime.utcnow() + timedelta(minutes=30)},
    #     app.config['SECRET_KEY'])
    # print (token.decode())
    print (token)
    response = {
        'token': token,
        'status': 'success'

    }
    return jsonify(response)


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                raise RuntimeError('User not found')
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401 # 401 is Unauthorized HTTP status code
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify




if __name__ == '__main__':
	from models import db
	db.init_app(app)
	app.run()
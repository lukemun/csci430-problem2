import sqlite3
from flask import Flask, g

from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from models import *


# configuration
DEBUG = True
DATABASE = "database.db"
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
# used for encryption and session management
SECRET_KEY = 'mysecretkey'

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

@app.route('/register', methods=('POST',))
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# @app.route('/register', methods=['POST'])
# def register():
# 	response = {}
# 	post_data = request.get_json()
# 	username = post_data.get('username')
# 	password = post_data.get('password')

	# db = get_db()
	# known_users = db.execute('select * from users where username = ?', [username])
	# print ('known', known_users)
	# num_users = known_users.fetchall()
	# print (len(num_users))
	# if (len(num_users) != 0):
	# 	print ('here')
	# 	response['error'] = "Username taken"
	# 	return jsonify(response)

	# db.execute(
	# 	'insert into users (username, password) values (?, ?)',
	# 	[username, password])

	# db.commit()
	# response['error'] = None
	# return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
	response = {}
	post_data = request.get_json()
	username = post_data.get('username')
	password = post_data.get('password')
	db = get_db()
	known_users = db.execute('select * from users where username = ?', [username])

	select_user = known_users.fetchone()
	# print (select_user.keys())
	if (select_user == None):
		print ('here')
		response['error'] = "User does not exist"
		return jsonify(response)

	saved_password = select_user['password']
	if (saved_password != password):
		response['error'] = "Incorrect password"
		return jsonify(response)


	response['error'] = None
	return jsonify(response)


if __name__ == '__main__':
	from models import db
	db.init_app(app)
	app.run()
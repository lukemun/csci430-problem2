#! /user/bin/python3.9

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/kyle/csci430-problem2/server')
from app import app as application
application.secret_key = 'bigbootyhoes'
from models import db
db.init_app(application)

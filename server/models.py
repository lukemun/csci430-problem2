import jwt, app
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    photo = db.relationship('Photo', backref="creator", lazy=False)

    def __init__(self, email, first_name, last_name, dob, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.password = generate_password_hash(password)
        print(self.password)

    @classmethod
    def authenticate(cls, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        
        if not email or not password:
            return None

        user = cls.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return None

        return user

    def encode_auth_token(self, email, secret_key):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=1),
                'iat': datetime.utcnow(),
                'sub': email,
            }
            return jwt.encode(
                payload,
                secret_key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token, secret_key):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """

        try:
            payload = jwt.decode(auth_token, secret_key, algorithms=['HS256'])
            print(payload)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def to_dict(self):
        return dict(id=self.id, email=self.email)

class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    file = db.Column(db.LargeBinary)
    creator_email = db.Column(db.String(255), db.ForeignKey('users.email'))

    def __init__(self, name, file, creator_email):
        self.name = name
        self.creator_email = creator_email
        self.file = bytes(file, 'utf-8')


    def to_dict(self):
      return dict(id=self.id,
                  file=self.file)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.secret_key = '34whiufgiug8342'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/valeska/Documents/icecreamapp/src/user.db'

db = SQLAlchemy(app)

class LoginException(Exception):
    def __init__(self, error):
        self.error = error
    def msg(self):
        return self.error

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    name = db.Column(db.String(100), unique=False)
    pw_hash = db.Column(db.String(300), unique=False)

    def __init__(self, username, password_hash, name):
        self.username = username
        self.pw_hash = password_hash
        self.name = name

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def _get_name(self):
        return self.name

    @staticmethod
    def user_exists(username):
        users = User.query.filter_by(username=username)
        return users.first()


    @staticmethod
    def create_user(username, unhashed_password, name):
        if not User.user_exists(username):
            db.session.add(User(username, generate_password_hash(unhashed_password), name))
            db.session.commit()
            return True
        return False

    @staticmethod
    def check_user_and_password(username, unhashed_password):
        user = User.user_exists(username)
        if user:
            if user.check_password(unhashed_password):
                return user 
            raise LoginException('wrong_password')
        raise LoginException('wrong_username')

    @staticmethod
    def get_name(username):
        user = user_exists(username)
        try:
            return user._get_name()
        except Exception as a:
            print (a)
            return False

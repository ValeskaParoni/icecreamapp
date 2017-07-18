from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import session, request, render_template, redirect

app = Flask(__name__, template_folder='../../templates', static_url_path='/static')
app.secret_key = '34whiufgiug8342'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/valeska/Documents/icecreamapp/src/user.db'

db = SQLAlchemy(app)


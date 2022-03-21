from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

bcrypt = Bcrypt(app)


app.config['SECRET_KEY'] = 'secret-key-goes-here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model.db'

db = SQLAlchemy(app)

from market import route
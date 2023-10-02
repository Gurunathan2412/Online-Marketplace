from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '5b668bd00fd3ca91fcca30e2'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = "login_page"
login.login_message_category = 'info'

from market import routes

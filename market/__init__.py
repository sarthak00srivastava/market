from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '444444444444444444444444'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please Log In to continue.'
login_manager.login_message_category = 'info'

from market import models

from market import routes
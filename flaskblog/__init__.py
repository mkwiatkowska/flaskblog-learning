from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


#zainstancjonowanie appki flaskowej
app = Flask(__name__)

#later make it env variable
app.config['SECRET_KEY'] = 'a8a1b7728c69b879f4c218afb8d49e36'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
#klasa bootstrapa
login_manager.login_message_category = 'info'

from flaskblog import routes

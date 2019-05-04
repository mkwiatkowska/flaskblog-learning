from flask import Flask
from flask_sqlalchemy import SQLAlchemy


#zainstancjonowanie appki flaskowej
app = Flask(__name__)

#later make it env variable
app.config['SECRET_KEY'] = 'a8a1b7728c69b879f4c218afb8d49e36'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
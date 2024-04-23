from dotenv import load_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

load_dotenv()
app = Flask(__name__)
# app=flask.Flask(__name__,template_folder='folder')
# by default the templates folder need to be named "templates"
# or we can specify the template_folder paramter when creating the flask application
#secrets.token_hex(16) 
app.config['SECRET_KEY']=os.getenv("secret")
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

from webflask import routes
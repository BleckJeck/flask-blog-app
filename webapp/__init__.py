from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(
  __name__,
  instance_relative_config = True,
  static_folder = 'static',
  template_folder = 'templates'
)

app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from . import views
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(
  __name__,
  instance_relative_config = True,
  static_folder = 'static',
  template_folder = 'templates'
)

app.config.from_object('config')
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from . import views
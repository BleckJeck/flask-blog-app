from flask import Flask, session, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps

def is_logged_in(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      flash('Unauthorized, please login', 'error')
      return redirect(url_for('main.login'))
  return wrap

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

from .views.main import main
from .views.blog import blog
from .views.users import users
from .views.trackme import trackme

app.register_blueprint(main)
app.register_blueprint(blog, url_prefix='/blog')
app.register_blueprint(users, url_prefix='/user')
app.register_blueprint(trackme, url_prefix='/trackme')
from flask import Flask, session, flash, redirect, url_for, render_template
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
from .views.recipes import recipes

app.register_blueprint(main)
app.register_blueprint(blog, url_prefix='/blog')
app.register_blueprint(users, url_prefix='/user')
app.register_blueprint(trackme, url_prefix='/trackme')
app.register_blueprint(recipes, url_prefix='/recipes')

# ERROR HANDLING

@app.errorhandler(403)
def error_403(error):
  return render_template('errors/403.html', title="403"), 403

@app.errorhandler(404)
def error_404(error):
  return render_template('errors/404.html', title="404"), 404

@app.errorhandler(405)
def error_405(error):
  return render_template('errors/405.html', title="405"), 405

@app.errorhandler(500)
def error_500(error):
  return render_template('errors/500.html', title="500"), 500
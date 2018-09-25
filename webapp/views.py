from flask import (
  render_template,
  url_for,
  flash,
  redirect,
  session
)
from functools import wraps
from . import app, db, bcrypt
from .forms import LoginForm, RegisterForm
from .models import User, Post

# Custom decorator to check if user is logged in
def is_logged_in(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      flash('Unauthorized, please login', 'error')
      return redirect(url_for('login'))
  return wrap

#########
# PUBLIC ROUTES
#########

@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html', title="Home")


@app.route("/about")
def about():
  return render_template('about.html', title="About")


@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      session['logged_in'] = True
      session['username'] = form.username.data
      flash(f"You're now logged in as {form.username.data}", "success")
      return redirect(url_for('admin'))
    else:
      flash('Login Unsuccessful. Please check username and password', 'error')
  return render_template('login.html', title="Login", form=form)


@app.route("/logout")
def logout():
  session.clear()
  flash("You've been successfully logged out", 'success')
  return redirect(url_for('home'))

#########
# PRIVATE ROUTES
#########

@app.route("/admin")
@is_logged_in
def admin():
  return render_template('admin-dashboard.html')


@app.route("/admin/register", methods=['GET', 'POST'])
@is_logged_in
def register():
  form = RegisterForm()
  if form.validate_on_submit():
    hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data,
    password=hashed_pwd)
    db.session.add(user)
    db.session.commit()
    flash(f'Account created for {form.username.data}!', 'success')
  return render_template('register.html', title="Register User", form=form)

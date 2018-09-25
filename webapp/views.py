from flask import (
  render_template,
  url_for,
  flash,
  redirect
)
from . import app
from .forms import LoginForm
from .models import User, Post

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
    # Dummy data to simulate login
    if form.email.data == 'test@test.com' and form.password.data == '1234':
      flash(f'{form.email.data} logged in succesfully!', 'success')
      return redirect(url_for('home'))
    else:
      flash('Invalid Email/Password', 'error')
  return render_template('login.html', title="Login", form=form)

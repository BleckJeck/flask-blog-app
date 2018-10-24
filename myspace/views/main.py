from flask import Blueprint, request, render_template, url_for, flash, redirect, session, abort

from .. import db, bcrypt, is_logged_in
from ..forms import LoginForm
from ..models import User

main = Blueprint('main', __name__)

@main.route("/")
def landing():
  return render_template('landing-page.html')

@main.route("/home")
def home():
  return render_template('home.html', title="Home")

@main.route("/docs")
def documentation():
  return render_template('docs.html', title="Docs")

# DASHBOARD AREA
@main.route("/admin")
@is_logged_in
def admin():
  return render_template('admin-dashboard.html', title="Admin Area")

# LOGIN
@main.route("/login", methods=['GET', 'POST'])
def login():
  if 'logged_in' in session:
    return redirect(url_for('.admin'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      session['logged_in'] = True
      session['username'] = form.username.data
      flash(f"You're now logged in as {form.username.data}", "success")
      return redirect(url_for('.admin'))
    else:
      flash('Login Unsuccessful. Please check username and password', 'error')
  return render_template('login.html', title="Login", form=form)

# LOGOUT
@main.route("/logout")
@is_logged_in
def logout():
  session.clear()
  flash("You've been successfully logged out", 'success')
  return redirect(url_for('.home'))

# ERROR HANDLING
@main.errorhandler(404)
def error_404(error):
  return render_template('404.html'), 404

@main.errorhandler(403)
def error_403(error):
  return render_template('403.html'), 403

@main.errorhandler(500)
def error_500(error):
  return render_template('500.html'), 500


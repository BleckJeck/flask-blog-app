from flask import Blueprint, request, render_template, url_for, flash, redirect, session, abort

from .. import db, bcrypt, is_logged_in
from ..forms import RegisterForm, UpdateUserForm
from ..models import User

users = Blueprint('users', __name__)

# CREATE USER
@users.route("/new", methods=['GET', 'POST'])
@is_logged_in
def register():
  form = RegisterForm()
  users = User.query.all()
  curr_user = session['username']
  if form.validate_on_submit():
    hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data,
    password=hashed_pwd)
    db.session.add(user)
    db.session.commit()
    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('.register'))
  return render_template('users/register.html', title="Register User", form=form, users=users, curr_user=curr_user)

# UPDATE USER
@users.route("/<int:user_id>/update", methods=['GET', 'POST'])
@is_logged_in
def update_user(user_id):
  user = User.query.get_or_404(user_id)
  if user.username != session['username']:
    abort(403)
  form = UpdateUserForm()
  users = User.query.all()
  if form.validate_on_submit():
    session['username'] = form.username.data
    user.username = form.username.data
    user.email = form.email.data
    db.session.commit()
    flash(f'Account updated for {form.username.data}!','success')
    return redirect(url_for('.register'))
  elif request.method == 'GET':
    form.username.data = user.username
    form.email.data = user.email
  return render_template('users/update-user.html', title="Update User", form=form, users=users)

# DELETE USER
@users.route("/<int:user_id>/delete", methods=['POST'])
@is_logged_in
def delete_user(user_id):
  user = User.query.get_or_404(user_id)
  if user.username != session['username']:
    abort(403)
  db.session.delete(user)
  db.session.commit()
  return redirect(url_for('main.logout'))


from flask import (
  request,
  render_template,
  url_for,
  flash,
  redirect,
  session,
  abort
)
from functools import wraps
from . import app, db, bcrypt
from .forms import LoginForm, RegisterForm, PostForm
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


@app.route("/blog")
def blog():
  posts = Post.query.all()
  return render_template('blog.html', title="Blog", posts=posts)


@app.route("/blog/<int:post_id>")
def post(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post-r.html', title=post.title, post=post)


@app.route("/login", methods=['GET', 'POST'])
def login():
  if 'logged_in' in session:
    return redirect(url_for('admin'))
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

# ERROR HANDLING
@app.errorhandler(404)
def error_404(error):
  return render_template('404.html'), 404

@app.errorhandler(403)
def error_403(error):
  return render_template('403.html'), 403

@app.errorhandler(500)
def error_500(error):
  return render_template('500.html'), 500


#########
# PRIVATE ROUTES
#########

# DASHBOARD AREA
@app.route("/admin")
@is_logged_in
def admin():
  return render_template('admin-dashboard.html', title="Admin Area")


# LOGOUT
@app.route("/logout")
@is_logged_in
def logout():
  session.clear()
  flash("You've been successfully logged out", 'success')
  return redirect(url_for('home'))


# ADD NEW USER
@app.route("/admin/register", methods=['GET', 'POST'])
@is_logged_in
def register():
  form = RegisterForm()
  users = User.query.all()
  if form.validate_on_submit():
    hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, email=form.email.data,
    password=hashed_pwd)
    db.session.add(user)
    db.session.commit()
    flash(f'Account created for {form.username.data}!', 'success')
    return redirect(url_for('register'))
  return render_template('register.html', title="Register User", form=form, users=users)


# CREATE NEW POST
@app.route("/admin/post/new", methods=['GET', 'POST'])
@is_logged_in
def new_post():
  form = PostForm()
  posts = Post.query.filter_by(user_id=session['username']).all()
  if form.validate_on_submit():
    author = session['username']
    post = Post(title=form.title.data, content=form.content.data,
    user_id=author)
    db.session.add(post)
    db.session.commit()
    flash('Post Created!', 'success')
    return redirect(url_for('blog'))
  return render_template('post-cu.html', title="New Post", form=form, posts=posts)


# UPDATE POST
@app.route("/admin/post/<int:post_id>/update", methods=['GET', 'POST'])
@is_logged_in
def update_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.user_id != session['username']:
    abort(403)
  form = PostForm()
  posts = Post.query.filter_by(user_id=session['username']).all()
  if form.validate_on_submit():
    post.title = form.title.data
    post.content = form.content.data
    db.session.commit()
    flash('Post Updated','success')
    return redirect(url_for('post', post_id=post.id))
  elif request.method == 'GET':
    form.title.data = post.title
    form.content.data = post.content
  return render_template('post-cu.html', title="Update Post", form=form, posts=posts)


# DELETE POSTS
@app.route("/admin/post/<int:post_id>/delete", methods=['POST'])
@is_logged_in
def delete_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.user_id != session['username']:
    abort(403)
  db.session.delete(post)
  db.session.commit()
  flash('Post Deleted','success')
  return redirect(url_for('blog'))
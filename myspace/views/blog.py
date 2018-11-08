from flask import Blueprint, request, render_template, url_for, flash, redirect, session, abort

from .. import db, is_logged_in
from ..forms import PostForm
from ..models import Post

blog = Blueprint('blog', __name__)

# ALL POSTS
@blog.route("")
def all_posts():
  posts = Post.query.all()
  return render_template('blog/blog.html', title="Blog", posts=posts)

# SINGLE POST
@blog.route("/<int:post_id>")
def single_post(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('blog/post-r.html', title=post.title, post=post)

# CREATE POST
@blog.route("/new", methods=['GET', 'POST'])
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
    return redirect(url_for('.all_posts'))
  return render_template('blog/post-cu.html', title="New Post", form=form, posts=posts)

# UPDATE POST
@blog.route("/<int:post_id>/update", methods=['GET', 'POST'])
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
    return redirect(url_for('.single_post', post_id=post.id))
  elif request.method == 'GET':
    form.title.data = post.title
    form.content.data = post.content
  return render_template('blog/post-cu.html', title="Update Post", form=form, posts=posts)

# DELETE POST
@blog.route("/<int:post_id>/delete", methods=['POST'])
@is_logged_in
def delete_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.user_id != session['username']:
    abort(403)
  db.session.delete(post)
  db.session.commit()
  flash('Post Deleted','success')
  return redirect(url_for('.all_posts'))
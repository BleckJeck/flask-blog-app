from datetime import datetime
from . import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  posts = db.relationship('Post', backref='author', lazy=True)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  content = db.Column(db.Text, nullable=False)
  
  user_id = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)

  def __repr__(self):
    return f"Post('{self.title}', '{self.date_posted}')"

class Location(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  lat = db.Column(db.Float, nullable=False)
  lon = db.Column(db.Float, nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

  def __repr__(self):
    return f"Location('{self.lat}', '{self.lon}', '{self.date_posted}')"

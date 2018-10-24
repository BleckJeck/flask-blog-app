from flask import Blueprint, url_for, flash, redirect, session

from .. import db
from ..models import Location

trackme = Blueprint('trackme', __name__)

@trackme.route("/<int:lat>:<int:lon>", methods=['POST'])
def track(lat, lon):
  pos = Location(lat=lat, lon=lon)
  db.session.add(pos)
  db.session.commit()
  flash('Position Saved!', 'success')
  return redirect(url_for('main.landing'))
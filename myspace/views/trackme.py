from flask import Blueprint, request, render_template, url_for, flash, redirect, session, jsonify

from .. import db, is_logged_in
from ..models import Location
from ..forms import LocationForm

trackme = Blueprint('trackme', __name__)

# STANDARD VIEW (HANDLES NEW REQUESTS)
@trackme.route("", methods=['GET', 'POST'])
def new_location():
  form = LocationForm()
  if 'logged_in' in session and request.method == 'POST':
    if form.validate_on_submit():
      user = session['username']
      place = (form.location.data if form.location.data else None)
      pos = Location(lat=form.lat.data, lon=form.lon.data, accuracy=form.accuracy.data, user_name=user, place=place)
      db.session.add(pos)
      db.session.commit()
      flash('Position Saved!', 'success')
      return redirect(url_for('.new_location'))
    else:
      flash('Invalid Coordintes! Please try again', 'error')
  return render_template('trackme/trackme.html', title="TrackMe", form=form)

# LOCATIONS API
@trackme.route("/locations/api/v0.1", methods=['GET'])
def get_locations():
  if 'user' in request.args:
    locations = Location.query.filter_by(user_name=request.args['user']).all()
  else:
    locations = Location.query.all()

  # build json response
  data = []
  for location in locations:
    data.append({
      'lat': location.lat,
      'lon': location.lon,
      'accuracy': location.accuracy,
      'place': location.place,
      'date': location.date_posted,
      'user': location.user_name
    })
  resp = jsonify(data)
  resp.status_code = 200
  return resp
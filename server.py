from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from datetime import datetime
import time
#from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Entry, Trip, Location, Note
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.uploader import upload

app = Flask(__name__)

app.config.from_pyfile('config.py')

cloudinary.config(
  cloud_name = app.config['CLOUDINARY_CLOUD_NAME'],  
  api_key = app.config['CLOUDINARY_API_KEY'],  
  api_secret = app.config['CLOUDINARY_API_SECRET']  
)


# Raises an error so an undefined variable doesn't fail silently
app.jinja_env.undefined = StrictUndefined

app.jinja_env.auto_reload = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route("/")
def homepage():
	"""Homepage with login or create profile."""

	return render_template("welcome_page.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
	"""User registration/create a profile page"""

	if request.method == "POST":

		fname = request.form["fname"]
		lname = request.form["lname"]
		email = request.form["email"]
		password = request.form["password"]
		passwordConf = request.form['passwordConf']
		
		if password == passwordConf:
			new_user = User(fname=fname, lname=lname, email=email)
			new_user.create_password(password)
		else:
			del new_user['passwordConf']

		db.session.add(new_user)
		db.session.commit()

		user_id = new_user.user_id
		session["user_id"] = user_id

		return redirect(f"/user_journal/{user_id}")
	else:
		return redirect("/")


@app.route("/api/auth", methods=["POST"])
def login_process():
	"""Have a user login."""
		
	user = User.query.filter_by(email=request.form.get('email')).first()
	user_id = user.user_id
	
	if user.is_valid_password(request.form.get('password')):
	#if user.password == (request.form.get('password')):
		session['user_id'] = user.user_id
		return redirect(f"/user_journal/{user_id}")
	else:
		return redirect("/")


@app.route("/logout")
def logout():
	"""User logout."""

	del session["user_id"]
	flash("Logged out.")
	return redirect(f"/")

@app.route("/user_journal/<int:user_id>")
def user_journal(user_id):
	"""This is the user's journal homepage."""
	 
	trips = Trip.query.filter_by(user_id=user_id).all()
	locations = Location.query.filter_by(user_id=user_id).all()
	entries = Entry.query.filter_by(user_id=user_id).all()
	notes= Note.query.filter_by(user_id=user_id).all()

	return render_template("users_journal.html",
						   trips=trips,
						   user_id=user_id,
						   locations=locations,
						   entries=entries,
						   notes=notes)


@app.route("/create_trip", methods=["GET","POST"])
def create_trip():
	"""Create a new trip."""

	if request.method == "POST":

		user_id = session["user_id"]
		trip_name = request.form["trip_name"]
		description = request.form["description"]
		trip = Trip(trip_name=trip_name, description=description, user_id=user_id)

		db.session.add(trip)
		db.session.commit()
		trip_id = trip.trip_id
		flash("Your trip has been added!")

		return redirect(f"/user_journal/{user_id}") 

	else:
		return render_template("create_trip.html")

	if request.method == "GET": 
										
		user_id = session["user_id"]

		return redirect(f"/create_trip/{trip_id}")


@app.route("/trip/<int:trip_id>")
def get_trip(trip_id):
	"""Search for a trip from a master list.****"""
	
	
	trip = Trip.query.get(trip_id)
	name = trip.trip_name
	description = trip.description
	entries = trip.entries
	user_id = trip.user_id
	trips = []
	
	
	if user_id: 
		for trip in trips:
			trip_id = Trip.query.get(trip_id)
			name = trip.trip_name
			trips.append(name)

		return render_template("trip.html",
							trip=trip,
							name=name,
							description=description,
							user_id=user_id)


@app.route("/pictures")
def pictures():
	 
	user_id = session["user_id"]
	trips = Trip.query.filter_by(user_id=user_id).all()
	entries = Entry.query.filter_by(user_id=user_id).all()
	pictures = map(lambda entry: entry.user_picture, entries) 
	
	if user_id:

		return render_template("pictures.html",
								pictures=pictures)
	else:
		return redirect("/select_trip")


@app.route("/select_trip")
def select_trip():

	user_id = session["user_id"]
	trips = Trip.query.filter_by(user_id=user_id).all()

	next_route = request.args.get("next_route")

	return render_template("trips_selector.html",
							trips=trips,
							next_route=next_route)


@app.route("/add_location/<int:trip_id>", methods=["GET", "POST"])
def add_location(trip_id):
	"""Gather location information about a trip."""

	trip = Trip.query.get(trip_id)

	if request.method == "POST":
		user_id = session["user_id"]
		name = request.form["name"]
		address = request.form["address"]
		city = request.form["city"]
		state = request.form["state"]
		country = request.form["country"]

		location = Location(user_id=user_id,
							address=address,
							city=city,
							state=state,
							country=country,
							name=name)

		location.trips = [trip] # assoc table pop

		db.session.add(location)
		#if refactor with modelMixin, can do location.save
		db.session.commit()

		location_id = location.location_id

		flash("Your location has been added!")
		return redirect(f"/user_journal/{user_id}")

	else:
		return render_template("create_location.html",
								trip_id=trip_id)


@app.route("/locations/<int:location_id>")
def get_location(location_id):
	"""Search for a location from a master list****."""

	location = Location.query.get(location_id) 

	user_id = session["user_id"]
	if location.user_id != session["user_id"]:
		return redirect("/")

	return render_template("locations.html",
							location=location)


@app.route("/add_entry/<int:trip_id>", methods=["GET", "POST"])
def add_entry(trip_id):
	"""This is where the user can add an entry to their trip."""
	
	user_id = session["user_id"]
	
	if request.method == "POST":
		title = request.form["title"]
		text = request.form["entry"]
		upload = request.files["file"]

		all_numbers = datetime.now().timestamp()
		time_stamp = time.ctime(all_numbers)

		uploaded_file_info = cloudinary.uploader.upload(upload)
		image_url = uploaded_file_info['secure_url']


		entry = Entry(title=title,
					entry=text,
					user_id=user_id, 
					trip_id=trip_id,
					time_stamp=time_stamp,
					user_picture=image_url)

		db.session.add(entry)
		db.session.commit()

		flash("Your entry has been added!")
		return redirect(f"/user_journal/{user_id}")	

	else:
		return render_template("create_entry.html",
								trip_id=trip_id,
								user_id=user_id)

@app.route("/entry/<int:entry_id>")
def get_entry(entry_id):
	"""Search for entries from a master list.****"""

	entry = Entry.query.get(entry_id)
	
	if entry.user_id != session["user_id"]:
		return redirect("/")

	return render_template("entries.html",
							entry=entry)

@app.route("/add_note", methods=["GET", "POST"])
def add_note():
	"""User can add short notes to their homepage."""


	user_id = session["user_id"]

	if request.method == "POST":
	
		note = request.form["note"]

		new_note = Note(note=note, user_id=user_id)


		db.session.add(new_note)
		db.session.commit()

		return jsonify({"note_id": new_note.note_id, "note": new_note.note})
	else:
		return redirect(f"/")
							

# @app.route("/????/<int:note_id>")
# def get_note(note_id):
# 	"""If I want to make notes links"""

# 	note_obj = Note.query.get(note_id)
# 	note = note_obj.note
	
# 	if note.user_id != session["user_id"]:
# 		return jsonify({note})

# 	return jsonify({"no new note"})


# @app.route("/upload") #sandbox
# def upload_image():

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



if __name__ == '__main__':

	app.debug = True

	connect_to_db(app)

	#DebugToolbarExtension(app)

	app.run(host='0.0.0.0')
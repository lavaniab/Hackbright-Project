from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Entry, Trip, Location

app = Flask(__name__)

app.config.from_pyfile('config.py')

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
	# Get form variables
		fname = request.form["fname"]
		lname = request.form["lname"]
		email = request.form["email"]
		password = request.form["password"]
		new_user = User(fname=fname, lname=lname, email=email, password=password)


		db.session.add(new_user)
		db.session.commit()

		user_id = new_user.user_id
		app.logger.info(f"\n\n\n\n IN REGIS user_id={user_id}")
		session["user_id"] = user_id
	
		flash("New user profile created!")
		return redirect(f"/user_journal/{user_id}")
	else:
		return redirect(f"/")


@app.route("/api/auth", methods=["POST"])
def login_process():
	"""Have a user login."""
		#user.is_valid_password 65
	user = User.query.filter_by(email=request.form.get('email')).one()
	user_id = user.user_id
	if user.password == (request.form.get('password')):
		session['user_id'] = user.user_id
		flash('Login success!', 'success')
		return redirect(f"/user_journal/{user_id}")
	else:
		flash('Invalid password. Try again.', 'danger')
		return redirect("/")


@app.route("/logout")
def logout():
	"""User logout."""

	del session["email"]
	flash("Logged out.")
	return redirect(f"/")

@app.route("/user_journal/<int:user_id>")
def user_journal(user_id):
	"""This is the user's journal homepage."""
	
	trips = Trip.query.filter_by(user_id=user_id).all()
	app.logger.info(f"\n\n\n\n IN USER_JOUR user_id={user_id}")
	locations = Location.query.filter_by(user_id=user_id).all()
	# locations = []
	# for trip in trips:
	# 	for location in trip.locations:
	# 		locations.append(location)
	print("SDCVGBHGFDSASDFGFDSA" f"locations = {locations}")
	entries = Entry.query.filter_by(user_id=user_id).all()

	return render_template("users_journal.html",
						   trips=trips,
						   user_id=user_id,
						   locations=locations,
						   entries=entries)


@app.route("/create_trip", methods=["GET","POST"])
def create_trip():
	"""Create a new trip."""

	if request.method == "POST":

		user_id = session["user_id"]
		app.logger.info(f"\n\n\n\n iN CREATE_TRIP user_id={user_id}")
		trip_name = request.form["trip_name"]
		description = request.form["description"]
		app.logger.info(f"\n\n\n\n user_id={user_id}")
		trip = Trip(trip_name=trip_name, description=description, user_id=user_id)

		db.session.add(trip)
		db.session.commit()
		trip_id = trip.trip_id
		app.logger.info(f"\n\n\n\n IN CREATE_TRIP trip_id={trip_id}")
		flash("Your trip has been added!")
		session['trip_id'] = trip_id
		return render_template("create_location.html", trip_id=trip_id) #create_trip/<int:trip_id>") #{trip.trip_id}") # want to save on page, reload just this

	else:
		return render_template("create_trip.html")

	if request.method == "GET": #trying to separate out routes
										#moved this to def get_trip()
		user_id = session["user_id"]
		app.logger.info(f"\n\n\n\n IN CREATE_TRIP 'GET' user_id={user_id}")
		trips = []
		for trip in trips:
			trip_id = Trip.query.get(trip_id)
			app.logger.info(f"\n\n\n\n IN LOOP OF CREATE_TRIP 'GET' user_id={user_id}")
			name = trip.trip_name
			app.logger.info(f"\n\n\n\n name={name}")
			trips.append(name)

	return redirect(f"/create_trip/{trip_id}")


@app.route("/create_trip/<int:trip_id>")
def get_trip(trip_id):
	"""Page for certain trip with locations and entries available"""
	
	app.logger.info(f"\n\n\n\n IN GET_TRIP() trip_id={trip_id}")
	trip = Trip.query.get(trip_id) #returns query object, whole row of data
	name = trip.trip_name
	description = trip.description
	entries = trip.entries
	trips = []
	user_id = trip.user_id
	app.logger.info(f"\n\n\n\n IN GET_TRIP() user_id={user_id}")
	
	if user_id: # if user_id == session["user_id"]
		for trip in trips:
			trip_id = Trip.query.get(trip_id)
			app.logger.info(f"\n\n\n\n IN LOOP GET_TRIP() trip_id={trip_id}")
			name = trip.trip_name
			app.logger.info(f"\n\n\n\n IN LOOP GET_TRIP() name={name}")
			trips.append(name)

		return render_template("trips.html",
								trip=trip,
								name=name,
								description=description,
								entries=entries,
								user_id=user_id)

@app.route("/select_trip")
def select_trip():

	user_id = session["user_id"]
	trips = Trip.query.filter_by(user_id=user_id).all()

	return render_template("trips_selector.html", trips=trips)


@app.route("/add_location/<int:trip_id>", methods=["GET", "POST"])
def add_location(trip_id):
	"""Gather location information about a trip."""

	trip = Trip.query.get(trip_id)

	if request.method == "POST":
		user_id = session["user_id"]
		app.logger.info(f"\n\n\n\n IN ADD_LOCAT user_id={user_id}")
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

		location.trips = [trip]

		db.session.add(location)
		#if refactor with modelMixin, can do location.save
		db.session.commit()

		location_id = location.location_id
		app.logger.info(f"\n\n\n\n IN ADD_LOCAT location_id={location_id}")

		flash("Your location has been added!")
		return render_template("create_entry.html")

	else:
		return render_template("create_location.html", trip_id=trip_id)


@app.route("/locations/<int:user_id>")
def get_location(user_id):
	"""Search for a location."""


	location = Location.query.get(location_id) 
	trip =Trip.query.get(trip_id)
	user_id = trip.user_id #do I need this one if id is getting passed into fn
	name = location.name 
	address = location.address
	city = location.city
	state = location.state
	country = location.country
	
	locations = []
	
	if user_id:
		for location in locations:
			location = Location.query.get(location_id)
			name = location.name
			app.logger.info(f"\n\n\n\n IN GET_LOCAT name={name}")
			locations.append(name)
		return render_template("trips.html",
								trip=trip,
								name=name,
								address=address,
								city=city,
								state=state,
								country=country)


@app.route("/add_entry", methods=["POST"]) #<int:user_id>") removed GET
def add_entry():
	"""This is where the user can add an entry to their trip."""
	
	user_id = session["user_id"]
	# if request.method == "POST":
	text = request.form["entry"]

	entry = Entry(entry=text, user_id=session["user_id"], trip_id=session["trip_id"])

	db.session.add(entry)
	db.session.commit()

	flash("Your entry has been added!")
	return redirect(f"/user_journal/{user_id}")
	# else:
	# 	return redirect(f"/user_entry/{trip_id}")

@app.route("/user_entry/<int:user_id>")
def get_entry(user_id):
	"""Page for certain trip with locations and entries available"""
	
	entry_object = Entry.query.get(entry_id)
	user_id = entries.user_id
	entry_id = entries.entry_id
	app.logger.info(f"\n\n\n\n IN GET_ENTRY() user_id={user_id}")
	trip = Trip.query.get(trip_id)
	trip_id = entries.trip_id
	app.logger.info(f"\n\n\n\n IN GET_TRIP() trip_id={trip_id}")
	name = trip.trip_name
	entry = entries.entry

	entries = []
	
	if user_id == session["user_id"]:
		for entry in entries:
			if entry_id:
				app.logger.info(f"\n\n\n\n IN LOOP GET_TRIP() trip_id={trip_id}")
				name = trip.trip_name
				app.logger.info(f"\n\n\n\n IN LOOP GET_TRIP() name={name}")
				trips.append(name)

		return render_template("trips.html",
								trip=trip,
								name=name,
								entries=entries,
								user_id=user_id)


# @app.route("/sandbox/<int:trip_id>")
# def sandbox(trip_id):
# 	entry = Entry.query.filter_by(trip_id=trip_id).first()
# 	return(f"{entry.entry}")

if __name__ == '__main__':

	app.debug = True

	connect_to_db(app)

	DebugToolbarExtension(app)

	app.run(host='0.0.0.0')
from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
# from flask_sqlalchemy_session import flask_scoped_session, current_session
# session = flask_scoped_session(session_factory, app)
#from markupsafe import escape off of flask doc for flask login
#from flask_bootstrap import Bootstrap
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, BooleanField
#from wtforms.validators import InputRequired, Email, Length

from model import connect_to_db, db, User, Entry, Trip, Location, Locations_Trips

app = Flask(__name__)

app.config.from_pyfile('config.py')

# Raises an error so an undefined variable doesn't fail silently
app.jinja_env.undefined = StrictUndefined

app.jinja_env.auto_reload = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


@app.route("/")
def homepage():
	"""Homepage"""

	return render_template("homepage.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
	"""User registration/create a profile page"""

	if request.method == "POST":
	# Get form variables
		fname = request.form["fname"]
		lname = request.form["lname"]
		email = request.form["email"]
		password = request.form["password"]
		new_user = User(fname=fname, lname=lname, email=email,
						 password=password)


		db.session.add(new_user)
		db.session.commit()

		user_id = new_user.user_id
		print(f"\n\n\n\n user_id={user_id}")
		session["user_id"] = user_id
	
		flash("New user profile created!")
		return redirect(f"/user_journal/{new_user.user_id}")
	else:
		return redirect(f"/")

	

@app.route("/api/auth", methods=["GET", "POST"])
def login_process():
	"""Have a user login."""

	db.session() #?
	cursor = db.session.execute("SELECT user_id FROM users") #?

	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]

		user = User.query.filter_by(email=email).one()
		password = User.query.filter_by(password=password).one()
		user_id = User.query.filter_by(user_id=user_id).one()
		user_id = session["user_id"]

		if not user:
			flash(f"Email not yet registered.")
			return redirect(f"/")

		if user.password != password:
			flash(f"Incorrect password!")
			return redirect(f"/") 

		if user and user.password ==password:
			session["user_id"] = user.user_id
			
			if "user_id" in session:
				flash("Logged in!")
				return redirect(f"/user_journal/{user.user_id}")
		else:
			return redirect(f"/")
	else:
		redirect(f"/")  


@app.route("/logout")
def logout():
	"""User logout."""

	del session["email"]
	flash("Logged out.")
	return redirect(f"/")

@app.route("/user_journal/<int:user_id>")
def user_homepage(user_id):
	"""This is the user's homepage."""
	
	trips = Trip.query.filter_by(user_id=user_id)

	return render_template("users_journal.html", trips=trips, user_id=user_id)


@app.route("/user_trip", methods=["GET", "POST"])
def user_trip():
	"""Create a new trip."""

	if request.method == "POST":

		# user_id = User.query.filter_by(User.user_id=session["user_id"])
		user_id = session["user_id"]
		trip_name = request.form["trip_name"]
		description = request.form["description"]
		print(f"\n\n\n\n user_id={user_id}")
		trip = Trip(trip_name=trip_name, description=description, user_id=user_id)

		db.session.add(trip)
		db.session.commit()

		flash("Your trip has been added!")
		return redirect(f"/user_trip/{trip.trip_id}") # want to save on page, reload just this
	else:
		return render_template("create_trip.html")

@app.route("/user_trip/<int:trip_id>")
def get_trip(trip_id):
	"""Page for certain trip with locations and entries available"""
	#db.session() #?
	#cursor = db.session.execute("SELECT user_id FROM users") #?
	#db.session.commit(user_id)
	trip = Trip.query.filter_by(trip_id=trip_id).one()
	name = trip.trip_name
	description = trip.description
	entries = trip.trip_entries

	return render_template("trips.html", trip=trip, name=name,
							description=description, entries=entries)


@app.route("/user_location", methods=["GET", "POST"])
def trip_location():
	"""Gather location information about a trip."""

	if request.method == "POST":
	#user = db.session.query(User).filter_by(user_id="User.entry_id")
	#user = User.query.filter_by(email=email).one()
	#name = User.query.get(User.email)
		name = request.form["name"]
		address = request.form["address"]
		city = request.form["city"]
		state = request.form["state"]
		country = request.form["country"]

		location = Location(address=address, city=city, state=state, country=country, name=name)

		db.session.add(location)
		locations = Trip.query.filter_by(location_id=location_id)
		db.session.commit()
		flash("Your location has been added!")
		return render_template("create_entry.html")

	else:
		return redirect(f"/user_trip")


@app.route("/user_entry", methods=["GET", "POST"]) #<int:user_id>")
def create_entry():
	"""This is where the user can add an entry to their trip."""
	
	if request.method == "POST":

		user_id = session["user_id"]
		print(user_id)

		trip_id = db.session.query(Trip).filter_by(user_id=user_id).one() #along correct line
		entry = request.form["entry"]

		entry = Entry(entry=entry)

		db.session.add(entry)
		db.session.commit()

	#need a button on html that opens a text box to then have the entry submitted
	#need to commit entry to db
		flash("Your entry has been added!")
		return redirect(f"/user_journal")
	else:
		return redirect(f"/")


if __name__ == '__main__':

	app.debug = True

	connect_to_db(app)

	DebugToolbarExtension(app)

	app.run(host='0.0.0.0')
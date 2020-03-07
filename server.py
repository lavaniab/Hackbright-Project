from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
#from markupsafe import escape off of flask doc for flask login
#from flask_bootstrap import Bootstrap
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, BooleanField
#from wtforms.validators import InputRequired, Email, Length

from model import connect_to_db, db, User, Entry, Trip, Location, Locations_Trip

#import model
app = Flask(__name__)

app.config.from_pyfile('config.py')

# Raises an error so an undefined variable doesn't fail silently
app.jinja_env.undefined = StrictUndefined

# This option will cause Jinja to automatically reload templates if they've been
# changed. This is a resource-intensive operation though, so it should only be
# set while debugging.
app.jinja_env.auto_reload = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# thank you flask documentation, got rid of the redirect error page 
# Required to use Flask sessions and the debug toolbar


@app.route("/")
def homepage():
	"""Homepage"""

	return render_template("homepage.html")

# @app.route("/")
# def register_process():
# 	"""Create a user profile."""



# 	#flash(f"User {email} added.")
# 	return render_template("homepage.html") #/{new_user.user_id}") ## is this equiv to the user_id col?
	

@app.route("/registration", methods=["GET", "POST"])
def login_form():
	"""User registration/create a profile page"""
	if request.method == "POST":
	# Get form variables
		fname = request.form["fname"]
		lname = request.form["lname"]
		email = request.form["email"]
		password = request.form["password"]

		new_user = User(fname=fname, lname=lname, email=email, password=password)

		db.session.add(new_user)
		db.session.flush()
		#print(new_user.user_id)
		db.session.commit()
		session["user_id"] = new_user.user_id
		flash("New user profile created!")
		return render_template("users_journal.html")
	else:
	#session["user_id"] = request.args.get("User.user_id")
		return redirect("/")

	

@app.route("/api/auth", methods=["GET", "POST"])
def login_process():
	"""Have a user login."""

	if request.method == "POST":

		email = request.form["email"]
		password = request.form["password"]
		user = User.query.filter_by(email=email).one()

		if not user:
			flash(f"Email not yet registered.")
			return redirect("/")

		if user.password != password:
			flash(f"Incorrect password!")
			return redirect("/") ## want to reload this spot on same page vs redirect

		if user and user.password ==password:								#ajax request ajax goes in html file?
			session["email"] = email
			
			if "user_id" in session:
				flash("Logged in!")
				return redirect("/user_journal")
		else:
			return redirect("/")
	else:
		redirect("/")
	
	##return render_template("user.html", email=email, password=password)
	#pass  


@app.route("/logout")
def logout():
	"""User logout."""

	del session["email"]
	flash("Logged out.")
	return redirect("/")

@app.route("/user_journal")
def user_homepage():
	"""This is the user's homepage."""

	if request.method == "GET":
		name = request.args.get("yes") #?
		return render_template("trip.html")
	else:
		return redirect("/")


@app.route("/user_trip", methods=["GET", "POST"])
def user_trip():

	if request.method == "POST":

		user_id = session["user_id"] #does not work
		trip_name = request.form["trip_name"]
		description = request.form["description"]

		trip = Trip(trip_name=trip_name, description=description)

		db.session.add(trip)
		db.session.commit()
		flash("Your trip has been added!")
		return render_template("location.html") # want to save on page, reload just this
	else:
		return redirect("users_journal.html")


@app.route("/user_location", methods=["GET", "POST"])
def user_location():
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
		db.session.commit()
		flash("Your location has been added!")
		return render_template("entry.html")

	else:
		return render_template("user.html") ##unsure of the else


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
		return render_template("users_journal.html")
	else:
		return redirect("/")


if __name__ == '__main__':

	app.debug = True

	connect_to_db(app)

	DebugToolbarExtension(app)

	app.run(host='0.0.0.0')
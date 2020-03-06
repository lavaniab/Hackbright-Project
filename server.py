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
	

@app.route("/login", methods=["POST"])
def login_form():
	"""User log in page"""

	# Get form variables
	fname = request.form["fname"]
	lname = request.form["lname"]
	email = request.form["email"]
	password = request.form["password"]

	new_user = User(fname=fname, lname=lname, email=email, password=password)

	db.session.add(new_user) 
	db.session.commit()


	#session["user_id"] = request.args.get("User.user_id")
	return render_template("login_form.html")

	

@app.route("/api/auth", methods=["POST"])
def login_process():
	"""Have a user login/create a profile."""


	# Get form variables
	email = request.form["email"]
	password = request.form["password"]
	user = User.query.filter_by(email=email).one()

	if not user:
		flash(f"Email not yet registered.")
		return redirect("/login")

	if user.password != password:
		flash(f"Incorrect password!")
		return redirect("/login") ## want to reload this spot on same page vs redirect

	if user and user.password ==password:								#ajax request ajax goes in html file?
		session["email"] = email
		flash("Logged in!")
		if "user_id" in session:
			return redirect("/user")
	else:
		return render_template("login_form.html")

	
	######return render_template("user.html", email=email, password=password)
	#pass  


@app.route("/logout")
def logout():
	"""User logout."""

	del session["email"]
	flash("Logged out.")
	return redirect("/")


@app.route("/user")
def user_page():
	"""This is the user's homepage."""


	#user = db.session.query(User).filter_by(user_id="User.entry_id")
	user = User.query.filter_by(email=email).one()
	#name = User.query.get(User.email)

	return render_template("user.html"user=user)

	# fn in here to make a new trip log in journal
	# save it then have the option to write an entry, send to 
	# return render_template("entry.html")

@app.route("/user_entry") #<int:user_id>")
def create_entry():
	"""This is where the user can add an entry to their trip."""

	#user = db.session.query(User).filter_by(user_id="User.entry_id") #relationship query?
	#entry = db.session.query(Entry).filter_by(user_id="user")

	#need a button on html that opens a text box to then have the entry submitted
	#need to commit entry to db
	#db.session.add(entry_id)
	#db.session.commit()

	return render_template("users_journal.html")


if __name__ == '__main__':

	app.debug = True

	connect_to_db(app)

	DebugToolbarExtension(app)

	app.run(host='0.0.0.0')
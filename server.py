from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Entry, Trip, Location, Association_Table

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

@app.route("/")
def register_process():
	"""Create a user profile."""

	# Get form variables
	fname = request.form["fname"]
	lname = request.form["lname"]
	email = request.form["email"]
	password = request.form["password"]

	new_user = User(fname=fname, lname=lname, email=email, password=password)

	db.session.add(new_user) 
	db.session.commit()

	# flash(f"User {email} added.")
	return redirect(f"/users/{new_user.user_id}") ## is this equiv to the user_id col?


@app.route("/login", methods=["GET"])
def login_form():
	"""User log in page"""

	return render_template("login_form.html")

@app.route("/login, methods=['POST']")
def login_process():

	# Get form variables
	email = request.form["email"]
	password = request.form["password"]

	user = User.query.filter_by(email=email).first()

	if not user:
		flash(f"Email not yet registered.")
		return redirect("/login")

	if user.password != password:
		flash(f"Incorrect password!")
		return redirect("/login") ## want to reload this spot on same page vs redirect

	session["user_id"] = user.user_id

	flash(f"Logged in!")
	return redirect(f"/users/{user.user_id}", email=email, password=password)



@app.route("/logout")
def logout():
	"""User logout."""

	del session["user_id"]
	flash(f"Logged out.")
	return redirect("/")


@app.route("/users/<int:user_id>")
def user_page():
	"""This is the user's homepage."""

	user = User.query.options(db.joindedload("users").joinedload("entries")).get(user_id)
	fname = User.query.get(fname)
	return render_template("user.html", user=user, fname=name)

	# fn in here to make a new trip log in journal
	# save it then have the option to write an entry, send to 
	# return render_template("entry.html")

@app.route("/users/<int:user_id>")
def create_entry():
	"""This is where the user can add an entry to their trip."""

	user = db.session.query(User).filter_by(user_id="User.entry_id") #relationship query?
	entry = db.session.query(Entry).filter_by(user_id="user")

	return render_template("users_journal.html")


if __name__ == '__main__':

	app.debug = True

	connect_to_db(app)

	DebugToolbarExtension(app)

	app.run(host='0.0.0.0')
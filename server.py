from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
# from flask_debugtoolbar import DebugToolbarExtention

from model import connect_to_db, db, User, Entry, Trip, Location

app = Flask(__name__)

# app.secret_key = "something"

# Raises an error so an undefined variable doesn't fail silently
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
	"""Homepage"""

	return render_template("some.html")

@app.route("/"):
def create_login():
	"""Create a user profile."""

	# Get form variables
	fname = request.form["fname"]
	lname = request.form["lname"]
	email = request.form["email"]
	password = request.form["password"]

	new_user = User(fname=fname, lname=lname, email=email, password=password)

	db.session.add(new_user)
	db.session.commit()


@app.route("/login_form", methods=["POST"])
def login_form():
	"""User log in page"""

	if user not in db:
		create user in db
	else:
		if email and password == self.email and self.password
		let them log in to their page
	return render_template("/{user_page}")
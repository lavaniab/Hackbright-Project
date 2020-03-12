"""Models and database functions for Travel Journal"""
from flask import Flask 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy, Model


#This is the connection to PostgreSQL database from library
#Find session object within where we do most of our interactions (like committing)

SQLALCHEMY_DATABASE_URI = "postgresql:///Travel_journaldb" # Unsure of what this does, also...table names or??
db = SQLAlchemy()

class User(db.Model):
	"""User of travel journal site"""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.String(25), nullable=False)
	lname = db.Column(db.String(25), nullable=False)
	email = db.Column(db.String(64), unique=True)
	password = db.Column(db.String(64), nullable=False)

	def __repr__(self):

		return f"<User user_id={self.user_id} email={self.email}>"


class Trip(db.Model):
	"""Trip the user entered into journal."""

	__tablename__ = "trips"

	trip_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
	trip_name = db.Column(db.String(100), nullable=False)
	description = db.Column(db.String(160), nullable=True)

	entries = db.relationship("Entry", backref="trips")
	locations = db.relationship("Location", secondary="locations_trips", backref="trips")

	def __repr__(self):

		return f"<Trip trip_id={self.trip_id} and user_id={self.user_id}>"

class Location(db.Model): #for now this will just be a nice little box with saved info that appears
	"""Locations of the trip."""  # visions of a 'clickable' button that would take user to another page with the spot pointed out in a map

	__tablename__ = "locations"

	location_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
	name = db.Column(db.String(100), nullable=True)
	address = db.Column(db.String(100), nullable=True)
	city = db.Column(db.String(100), nullable=True)
	state = db.Column(db.String(100), nullable=True)
	country = db.Column(db.String(100), nullable=True)

	def __repr__(self):

		return f"<Location location_id={self.location_id} and user_id={self.user_id}>"

	# trips = db.relationship("Trip", secondary="locations_trips", backref="locations") 

class Entry(db.Model):
	"""Entry table for all the entries for a user."""

	__tablename__ = "entries"

	entry_id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
	trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"))
	title = db.Column(db.String(100), nullable = False)
	entry = db.Column(db.String(), nullable=False)
	time_stamp = db.Column(db.DateTime(), server_default=db.func.now(), server_onupdate=db.func.now())
	user_picture = db.Column(db.String(200), nullable=True) ## ref url for third party image hosting
	
	user = db.relationship("User", backref="entries")
	

	def __repr__(self):

		return f"<Entry entry_id={self.entry_id}>"


locations_trips = db.Table("locations_trips", 

	db.Column("location_id", db.Integer, db.ForeignKey("locations.location_id"), primary_key=True),
	db.Column("trip_id", db.Integer, db.ForeignKey("trips.trip_id"), primary_key=True))
###################################################################

def connect_to_db(app):
	"""Connect the database to our Flask app."""

	# Configure to use our PostgreSQL database
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Travel_journaldb' 
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_ECHO'] = True
	db.app = app
	db.init_app(app)

if __name__ == "__main__":

	from server import app

	connect_to_db(app)
	#db.drop_all()
	db.create_all()

	print("Connect to DB.")

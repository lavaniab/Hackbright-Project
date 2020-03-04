"""Models and database functions for Travel Journal"""
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy, Model  

#This is the connection to PostgreSQL database from library
#Find session object within where we do most of our interactions (like committing)
# app = Flask(__name__) Do I need this here if in server.py????

DB_URI = "postgresql:///Travel_journaldb" # Unsure of what this does, also...table names or??
db = SQLAlchemy()

# def connect_to_db(app, Travel_journaldb): #(app, db_name) #should I move to model.py??
#     """Connect to database."""

#     app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{Travel_journaldb}"
#     app.config["SQLALCHEMY_ECHO"] = True
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#     db.app = app
#     db.init_app(app)

class User(db.Model):
	"""User of travel journal site"""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	fname = db.Column(db.String(25), nullable=False)
	lname = db.Column(db.String(25), nullable=False)
	email = db.Column(db.String(64), nullable=False, unique=True)
	password = db.Column(db.String(64), nullable=False)

	def __repr__(self):

		return f"<User fname={self.fname} email={self.email}>"


class Entry(db.Model):
	"""Entry table for all the entries from users."""

	__tablename__ = "entries"

	entry_id = db.Column(db.String(100), autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
	user_entry = db.Column(db.String(1500), nullable=False)
	user_picture = db.Column(db.String(200), nullable=True) ## ref url for third party image hosting
	
	user_entry = db.relationship("User", backref="entries")

	def __repr__(self):

		return f"<Entry entry_id={self.entry_id}>"



class Trip(db.Model):
	"""Trip the user entered into journal."""

	__tablename__ = "trips"

	trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	entry_id = db.Column(db.Integer, db.ForeignKey("entries.entry_id"))
	location_id = db.Column(db.String(500), db.ForeignKey("locations.location_id"), nullable=True)
	user_description = db.Column(db.String(160), nullable=True)

	trip_entries = db.relationship("Entry", backref="trips")

class Location(db.Model): #for now this will just be a nice little box with saved info that appears
	"""Locations of the trip."""  # visions of a 'clickable' button that would take user to another page with the spot pointed out in a map

	__tablename__ = "locations"

	location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	address = db.Column(db.String(100), nullable=True)
	city = db.Column(db.String(100), nullable=True)
	state = db.Column(db.String(100), nullable=True)
	country = db.Column(db.String(100), nullable=True)

	locations = db.relationship("Trip", backref="locations") 


class Association_Table(db.Model):
	"""Association between trips and locations."""

	__tablename__ = "locationsTrips"

	locationsTrips_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	location_id = db.Column(db.Integer, db.ForeignKey("locations.location_id"))
	trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"))



#db.session.commit() #just added this to trouble shoot no tables appearing in psql
###################################################################

def connect_to_db(app):
	"""Connect the database to our Flask app."""

	# Configure to use our PostgreSQL database
	app.config['SQLALCHEMY_	DATABASE_URI'] = 'postgresql:///travel_journaldb' 
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_ECHO'] = True
	db.app = app
	db.init_app(app)

if __name__ == "__main__":

	# from flask import Flask
	from server import app
	# app = Flask(__name__)

	connect_to_db(app)
	db.create_all()
	print("Connect to DB.")

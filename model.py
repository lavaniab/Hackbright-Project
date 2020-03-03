"""Models and datavase functions for Travel Journal"""

from flask_sqlalchemy import SQLAlchemy 

#This is the connection to PostgreSQL database from library
#Find session object within where we do most of our interactions (like committing)

db = SQLAlchemy()

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

	__tablename__ = "entries"

	entry_id = db.Column(db.String(100), autoincrement=True, primary_key=True)
	user_id = db.Column(db.Integer, foreign_key=True(User.user_id))
	user_entry = db.Column(db.String(1500), nullable=False)
	user_picture = db.Column(db.LargeBinary, nullable=True) ## ???
	## unsure if valid, maybe a whole table closer to end of project

class Trip(db.Model):
	"""Trip the user entered into journal."""

	__tablename__ = "trips"

	trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	entry_id = db.Column(db.Integer, foreign_key=True(Entry.entry_id))
	location = db.Column(db.String(500), nullable=True)
	user_description = db.Column(db.String(160), nullable=True)


###################################################################

def connect_to_db(app):
	"""Connect the database to our Flask app."""

	# Configure to use our PostgreSQL database
	app.config['SQLALCHEMY_	DATABASE_URI'] = 'postgresql:///travel_journal' ##?
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_ECHO'] = True
	db.app = app
	db.init_app(app)

if __name__ == "__main__"

from server import app

connect_to_db(app)
print("Connect to DB.")

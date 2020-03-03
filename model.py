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
	user_picture = db.Column(db.URL(200), nullable=True) ## ref url for third party image hosting
	
	user_entry = db.relationship("User", backref="entries")


class Trip(db.Model):
	"""Trip the user entered into journal."""

	__tablename__ = "trips"

	trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	entry_id = db.Column(db.Integer, foreign_key=True(Entry.entry_id))
	location_id = db.Column(db.String(500),foreign_key=True(Location.location_id), nullable=True)
	user_description = db.Column(db.String(160), nullable=True)


class Location(db.Model): #for now this will just be a nice little box with saved info that appears
						  # visions of a 'clickable' button that would take user to another page with the spot pointed out in a map
	__tablename__ = "locations"

	location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	address = db.Column(db.String(100), nullable=True)
	city = db.Column(db.String(100), nullable=True)
	state = db.Column(db.String(100), nullable=True)
	country = db.Column(db.String(100), nullable=True)


db.create_all()

###################################################################

# def connect_to_db(app):
# 	"""Connect the database to our Flask app."""

# 	# Configure to use our PostgreSQL database
# 	app.config['SQLALCHEMY_	DATABASE_URI'] = 'postgresql:///travel_journal' 
# 	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 	app.config['SQLALCHEMY_ECHO'] = True
# 	db.app = app
# 	db.init_app(app)

# if __name__ == "__main__"

# from server import app

# connect_to_db(app)
# print("Connect to DB.")

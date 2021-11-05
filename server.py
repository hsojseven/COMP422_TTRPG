import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, abort, jsonify
from myforms import LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# set up DB
scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "ttrpg.sqlite3")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Unicode, nullable=False)
    password = db.Column(db.Unicode, nullable=False)
    characters = db.relationship('Character', backref='Characters')

class Game(db.Model):
    __tablename__ = 'Games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode, nullable=False)
    description = db.Column(db.Unicode, nullable=False)

class Character(db.Model):
    __tablename__ = 'Characters'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID=db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False) # FK
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    wisdom = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)

# Use to clear tables and edit structure
# WILL WIPE ALL DB DATA
db.drop_all()
db.create_all()
##########################

@app.route("/home/")
def home():
    return render_template("home.html")

# for now just put a string in the login page and you will login
@app.route("/", methods=["GET", "POST"])
def login():
	loginForm = LoginForm()
	if request.method == 'GET':
		return render_template("loginForm.html", form=loginForm)

	if request.method == "POST":
		if loginForm.validate():
			return redirect(url_for("home"))
		else:
			for field,error in loginForm.errors.items():
				flash(f"{field}: {error}")
			return redirect(url_for("login"))
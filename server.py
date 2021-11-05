import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, abort, jsonify
from myforms import GameForm, LoginForm
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
    name = db.Column(db.Unicode, nullable=False)
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

user1 = User(id=1, username="bobBuilder", password=1234)
user2 = User(id=2, username="laryLobster", password=1234)
user3 = User(id=3, username="davidV", password=1234)

char1 = Character(id=1, userID=user1.id, name="Grug", strength=24, dexterity=14, constitution=20, intelligence=0, wisdom=10, charisma=0)
char2 = Character(id=2, userID=user1.id, name="Valfore", strength=10, dexterity=16, constitution=16, intelligence=14, wisdom=13, charisma=24)
char3 = Character(id=3, userID=user2.id, name="Bobby", strength=10, dexterity=23, constitution=16, intelligence=16, wisdom=16, charisma=10)
char4 = Character(id=4, userID=user2.id, name="Zerashale", strength=20, dexterity=12, constitution=16, intelligence=16, wisdom=12, charisma=20)
char5 = Character(id=5, userID=user3.id, name="Cul'gal", strength=12, dexterity=13, constitution=12, intelligence=25, wisdom=18, charisma=16)

game1 = Game(id=1, name="Raiders", description="This game will be played MWF at 8pm.")
game2 = Game(id=2, name="Mists over Camelot", description="Game containing players that play a game sometimes.")
game3 = Game(id=3, name="Vault of Kal'thari", description="Venture into the vault where many never return. Become rich, or die trying.")

db.session.add_all((user1, user2, user3, char1, char2, char3, char4, char5, game1, game2, game3))
db.session.commit()
##########################

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

@app.route("/home/")
def home():
    return render_template("home.j2", gameList=db.session.query(Game).all())

# route to make a new game
@app.route("/addGame/", methods=["GET", "POST"])
def addGame():
	newGameForm = GameForm()
	if request.method == 'GET':
		return render_template("gameForm.j2", form=newGameForm)

	if request.method == "POST":
		if newGameForm.validate():
			game = Game(name=newGameForm.name.data, description=newGameForm.description.data)
			db.session.add(game)
			db.session.commit()
			return redirect(url_for("home"))
		else:
			for field,error in newGameForm.errors.items():
				flash(f"{field}: {error}")
			return redirect(url_for("addGame"))

@app.route("/game/", methods=["GET", "POST"])
def game():
	return "<h2> This will be a game </h2>"
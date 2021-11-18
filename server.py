import os
from flask import Flask, render_template, request, redirect, url_for, flash
from myforms import GameForm, LoginForm, RegisterForm, CharacterForm
from flask_login import UserMixin, LoginManager, login_required
from flask_login import login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from hashing import Hasher

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# set up DB
scriptdir = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(scriptdir, "ttrpg.sqlite3")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Prepare and connect the LoginManager to this app
app.login_manager = LoginManager()
app.login_manager.login_view = 'get_login'
@app.login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

# open and read the contents of the pepper file into your pepper key
pepfile = os.path.join(scriptdir, "pepper.bin")
with open(pepfile, 'rb') as fin:
  pepper_key = fin.read()
  
# create a new instance of Hasher using that pepper key
pwd_hasher = Hasher(pepper_key)
#-----------------------------------------------------------------------------------------
#------------------------------------- USER TABLE ----------------------------------------
#-----------------------------------------------------------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, nullable=False)
    password_hash = db.Column(db.LargeBinary) # hash is a binary attribute
    characters = db.relationship('Character', backref='Characters')
    games = db.relationship('Player', backref='Games')
    
     # make a write-only password property that just updates the stored hash
    @property
    def password(self):
        raise AttributeError("password is a write-only attribute")
    @password.setter
    def password(self, pwd):
        self.password_hash = pwd_hasher.hash(pwd)
    
    # add a verify_password convenience method
    def verify_password(self, pwd):
        return pwd_hasher.check(pwd, self.password_hash)
#-----------------------------------------------------------------------------------------
#------------------------------------- GAME TABLE ----------------------------------------
#-----------------------------------------------------------------------------------------
class Game(db.Model):
    __tablename__ = 'Games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    description = db.Column(db.Unicode, nullable=False)
    gamers = db.relationship('Player', backref='Gamers')
    #msgHistory = db.Column(db.Unicode, nullable=True)
#-----------------------------------------------------------------------------------------
#----------------------------------- CHARACTER TABLE -------------------------------------
#-----------------------------------------------------------------------------------------
class Character(db.Model):
    __tablename__ = 'Characters'
    id=db.Column(db.Integer, primary_key=True)
    userID=db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False) # FK
    name = db.Column(db.Unicode, nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    wisdom = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)
#-----------------------------------------------------------------------------------------
#----------------------------------- Player Table ----------------------------------------
#-----------------------------------------------------------------------------------------
class Player(db.Model):
    __tablename__='Players'
    id=db.Column(db.Integer, primary_key=True)
    userID=db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    gameID=db.Column(db.Integer, db.ForeignKey('Games.id'), nullable=False)
    role=db.Column(db.Integer, nullable=False) # 0=player, 1=DM

# Use to clear tables and edit structure
# WILL WIPE ALL DB DATA
#db.drop_all()
#db.create_all()

user1 = User(id=1, username="bobBuilding")
user2 = User(id=2, username="laryLobster")
user3 = User(id=3, username="davidV")

char1 = Character(id=1, userID=user1.id, name="Grug", strength=24, dexterity=14, constitution=20, intelligence=0, wisdom=10, charisma=0)
char2 = Character(id=2, userID=user1.id, name="Valfore", strength=10, dexterity=16, constitution=16, intelligence=14, wisdom=13, charisma=24)
char3 = Character(id=3, userID=user2.id, name="Bobby", strength=10, dexterity=23, constitution=16, intelligence=16, wisdom=16, charisma=10)
char4 = Character(id=4, userID=user2.id, name="Zerashale", strength=20, dexterity=12, constitution=16, intelligence=16, wisdom=12, charisma=20)
char5 = Character(id=5, userID=user3.id, name="Cul'gal", strength=12, dexterity=13, constitution=12, intelligence=25, wisdom=18, charisma=16)

game1 = Game(id=1, name="Raiders", description="This game will be played MWF at 8pm.")
game2 = Game(id=2, name="Mists over Camelot", description="Game containing players that play a game sometimes.")
game3 = Game(id=3, name="Vault of Kal'thari", description="Venture into the vault where many never return. Become rich, or die trying.")

player1 = Player(userID=user1.id, gameID=game1.id, role=0)

#db.session.add_all((user1, user2, user3, char1, char2, char3, char4, char5, game1, game2, game3, player1))
#db.session.commit()
#-----------------------------------------------------------------------------------------
#---------------------------------- REGISTER NEW USER ------------------------------------
#-----------------------------------------------------------------------------------------
@app.get('/register/')
def get_register():
    form = RegisterForm()
    return render_template('register.html', form=form)

@app.post('/register/')
def post_register():
    form = RegisterForm()
    if form.validate():
        # check if there is already a user with this username
        user = User.query.filter_by(username=form.username.data).first()
        # if the username is free, create a new user and send to login
        if user is None:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('get_login'))
        else: # if the username already exists
            # flash a warning message and redirect to get registration form
            flash('There is already an account with that username')
            return redirect(url_for('get_register'))
    else: # if the form was invalid
        # flash error messages and redirect to get registration form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_register'))
#-----------------------------------------------------------------------------------------
#------------------------------------ USER LOG-IN ----------------------------------------
#-----------------------------------------------------------------------------------------
@app.get("/")
def get_login():
    login_form = LoginForm()
    return render_template("loginForm.html", form=login_form)

@app.post("/")
def post_login():
    form = LoginForm()
    if form.validate():
        # try to get the user associated with this username
        user = User.query.filter_by(username=form.username.data).first()
        # if this user exists and the password matches
        if user is not None and user.verify_password(form.password.data):
            # log this user in through the login_manager
            login_user(user)
            # redirect the user to the page they wanted or the home page
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('home')
            return redirect(next)
        else: # if the user does not exist or the password is incorrect
            # flash an error message and redirect to login form
            flash('Invalid username or password')
            return redirect(url_for('get_login'))
    else: # if the form was invalid
        # flash error messages and redirect to get login form again
        for field, error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_login'))
#-----------------------------------------------------------------------------------------
#-------------------------------------- HOME ROUTE ---------------------------------------
#-----------------------------------------------------------------------------------------
@app.route("/home/")
@login_required
def home():
    gameList=db.session.query(Game, Player).join(Game, Game.id==Player.gameID).filter(Player.userID == current_user.id).all()
    return render_template("home.html", gameList=gameList, user=current_user)
#-----------------------------------------------------------------------------------------
#-------------------------------------- CHARACTER ROUTE ----------------------------------
#-----------------------------------------------------------------------------------------
@app.route("/viewCharacters/")
@login_required
def viewCharacters():
    characterList=db.session.query(Character).filter(Character.userID == current_user.id).all()
    return render_template("viewCharacters.html", charList=characterList)
#-----------------------------------------------------------------------------------------
#-------------------------------------- ADD GAME -----------------------------------------
#-----------------------------------------------------------------------------------------
@app.route("/addGame/", methods=["GET", "POST"])
@login_required
def addGame():
    newGameForm = GameForm()
    if request.method == 'GET':
        return render_template("gameForm.html", form=newGameForm)

    if request.method == "POST":
        if newGameForm.validate():
            game = Game(name=newGameForm.name.data, description=newGameForm.description.data)
            db.session.add(game)
            db.session.commit()
            db.session.flush()

            player = Player(userID=current_user.id, gameID=game.id, role=1)
            db.session.add(player)
            db.session.commit()

            return redirect(url_for("home"))
        else:
            for field,error in newGameForm.errors.items():
                flash(f"{field}: {error}")
            return redirect(url_for("addGame"))

#-----------------------------------------------------------------------------------------
#----------------------------------- GAMEPLAY SCREEN -------------------------------------
#-----------------------------------------------------------------------------------------
@app.route("/<userID>/game/<gameID>", methods=["GET", "POST"])
@login_required
def game(userID, gameID):
    game = db.session.query(Game).filter(Game.id == gameID).first()
    username = db.session.query(User).filter(User.id == userID).first().username
    return render_template("gameScreen.html", game=game, username=username)


@app.route("/characters/", methods=["GET", "POST"])
@login_required
def get_characters():
    newCharacterForm = CharacterForm()
    if request.method == 'GET':
        return render_template("characterForm.html", form=newCharacterForm)
    if request.method == "POST":
        if newCharacterForm.validate():
            db.session.query(User, Character).join(User, User.id==Character.userID).all()
            character = Character(userID=current_user.id, name=newCharacterForm.name.data, 
                                strength=newCharacterForm.strength.data, dexterity=newCharacterForm.dexterity.data, 
                                constitution=newCharacterForm.constitution.data, intelligence=newCharacterForm.intelligence.data, 
                                wisdom=newCharacterForm.wisdom.data, charisma=newCharacterForm.charisma.data)
            db.session.add(character)
            db.session.commit()
            db.session.flush()
            return redirect(url_for("viewCharacters"))
        else:
            for field,error in newCharacterForm.errors.items():
                flash(f"{field}: {error}")
            return redirect(url_for("get_characters"))
#-----------------------------------------------------------------------------------------
#-------------------------------------- LOG OUT ------------------------------------------
#-----------------------------------------------------------------------------------------
@app.get('/logout/')
@login_required
def get_logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('get_login'))
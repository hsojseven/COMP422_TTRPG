import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import flask
import flask_login
import flask_socketio
import flask_sqlalchemy
from sqlalchemy.orm import session
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.util.langhelpers import NoneType
from myforms import GameForm, LoginForm, RegisterForm, CharacterForm, JoinWithIDForm, JoinGameForm, EditForm
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from hashing import Hasher
from werkzeug.utils import secure_filename
import json
import random
import string
from flask_socketio import SocketIO
from flask_socketio import emit, join_room, leave_room

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

#set up socket for chat messaging
socketio = SocketIO(app)

@socketio.on('joined', namespace='/game/')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = flask.session.get('room')
    join_room(room)
    #emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)

@socketio.on('text', namespace='/game/')
def text(message):
    print('MESSAGE RECEIEVED!')
    room = flask.session.get('room') 
    emit('message', {'msg': message['msg']}, room=room)
    


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
DEFAULT_BOARD = '{"attrs":{"width":958,"height":800},"className":"Stage","children":[{"attrs":{},"className":"Layer","children":[{"attrs":{"width":958,"height":783,"id":"BM"},"className":"Rect"},{"attrs":{"id":"greenBox","x":379,"y":386,"width":50,"height":50,"fill":"green","draggable":true,"stroke":"black"},"className":"Rect"},{"attrs":{"id":"redBox","x":450,"y":375,"width":50,"height":50,"fill":"red","draggable":true,"stroke":"black","visible":false},"className":"Rect"},{"attrs":{"id":"blueBox","x":450,"y":375,"width":50,"height":50,"fill":"blue","stroke":"black","draggable":true,"visible":false},"className":"Rect"},{"attrs":{"id":"yellowBox","x":450,"y":375,"width":50,"height":50,"fill":"yellow","stroke":"black","draggable":true,"visible":false},"className":"Rect"},{"attrs":{"id":"pinkBox","x":450,"y":375,"width":50,"height":50,"fill":"pink","stroke":"black","draggable":true,"visible":false},"className":"Rect"},{"attrs":{"id":"purpleBox","x":450,"y":375,"width":50,"height":50,"fill":"purple","stroke":"black","draggable":true,"visible":false},"className":"Rect"},{"attrs":{"id":"blackBox","x":450,"y":375,"width":50,"height":50,"fill":"black","stroke":"white","draggable":true,"visible":false},"className":"Rect"},{"attrs":{"id":"brownBox","x":450,"y":375,"width":50,"height":50,"fill":"brown","stroke":"black","draggable":true,"visible":false},"className":"Rect"},{"attrs":{"id":"tr"},"className":"Transformer"}]}]}'
class Game(db.Model):
    __tablename__ = 'Games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    description = db.Column(db.Unicode, nullable=False)
    board = db.Column(db.Unicode, nullable=True)
    imgUrl = db.Column(db.Unicode, nullable=True)
    gamers = db.relationship('Player', backref='Gamers')
    
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
#----------------------------------- PLAYER TABLE ----------------------------------------
#-----------------------------------------------------------------------------------------
class Player(db.Model):
    __tablename__='Players'
    id=db.Column(db.Integer, primary_key=True)
    userID=db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    gameID=db.Column(db.Integer, db.ForeignKey('Games.id'), nullable=False)
    role=db.Column(db.Integer, nullable=False) # 0=player, 1=DM

# Use to clear tables and edit structure
# WILL WIPE ALL DB DATA
# db.drop_all()
# db.create_all()
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
            flash('Thank you for Registering! Please log in.')
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
#--------------------------------------- HOME ROUTE --------------------------------------
#-----------------------------------------------------------------------------------------
@app.route("/home/", methods=["GET", "POST"])
@login_required
def home():
    newGameForm = GameForm()
    joinWithIDForm = JoinWithIDForm()
    joinGameForm = JoinGameForm()
    gameList = db.session.query(Game, Player).join(Game, Game.id==Player.gameID).filter(Player.userID == current_user.id).all()
    
    joinGameForm.characters.choices = [
        (items.id, items.name) for items in Character.query.all()]
    joinGameForm.games.choices=[
        (items[0].id, items[0].name) for items in gameList]
    
    if request.method == 'GET':
        return render_template("home.html", gameList=gameList, user=current_user, form=newGameForm, 
                               joinWithIDForm=joinWithIDForm, joinGameForm=joinGameForm)
    
    if request.method == "POST":
        if newGameForm.submit.data and newGameForm.validate():
            letters = string.ascii_letters
            imgName = ''.join(random.choice(letters) for i in range(20))
            
            image_data = request.files[newGameForm.map.name].read()
            path = f"./static/{imgName}.jpg"
            file = open(path, "wb")
            file.write(image_data)
            file.close()

            game = Game(name=newGameForm.name.data, description=newGameForm.description.data, board=DEFAULT_BOARD, imgUrl = path)
            db.session.add(game)
            db.session.commit()
            db.session.flush()

            player = Player(userID=current_user.id, gameID=game.id, role=1)
            db.session.add(player)
            db.session.commit()

            return redirect(url_for("home"))
        
        elif joinGameForm.validate():
            characterID = joinGameForm.characters.data
            gameID = joinGameForm.games.data
            return redirect(url_for("game", gameID=gameID, characterID=characterID))
            
        elif joinWithIDForm.submitJoin.data and joinWithIDForm.validate():
            player = Player(userID=current_user.id, gameID=joinWithIDForm.game.data, role=0)
            db.session.add(player)
            db.session.commit()
            db.session.flush()
            return redirect(url_for("home"))
        else:
            for field,error in newGameForm.errors.items():
                flash(f"{field}: {error}")
            return redirect(url_for("addGame"))
#-----------------------------------------------------------------------------------------
#-------------------------------------- CHARACTER ROUTE ----------------------------------
#-----------------------------------------------------------------------------------------
@app.route("/viewCharacters/", methods=["GET", "POST", "PUT"])
@login_required
def viewCharacters():
    newCharacterForm = CharacterForm()
    editForm = EditForm()
    characterList=db.session.query(Character).filter(Character.userID == current_user.id).all()
    if request.method == 'GET':
        return render_template("viewCharacters.html", form=newCharacterForm, charList=characterList, editForm = editFormx)
    
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
            return redirect(url_for("viewCharacters"))
    if request.method == "PUT":
        db.session.query(User, Character).join(User, User.id==Character.userID).all()
        editForm.name.data = "Bob"
        editForm.strength.data = "Bob"
        editForm.dexterity.data = "Bob"
        editForm.constitution.data = "Bob"
        editForm.intelligence.data = "Bob"
        editForm.wisdom.data = "Bob"
        editForm.charisma.data = "Bob"
        
        if editForm.validate():
            char = characterList.query.get(id)
            char.name = editForm.name.data
            char.strength = editForm.name.data
            char.dexterity = editForm.name.data
            char.constitution = editForm.constitution.data
            char.intelligence = editForm.intelligence.data
            char.wisdom = editForm.wisdom.data
            char.charisma = editForm.charisma.data
            db.session.commit()
            return redirect(url_for("viewCharacters", editForm = editForm))
        else:
            for field,error in newCharacterForm.errors.items():
                flash(f"{field}: {error}")
            return redirect(url_for("viewCharacters"))
#-----------------------------------------------------------------------------------------
#----------------------------------- GAMEPLAY SCREEN -------------------------------------
#-----------------------------------------------------------------------------------------
@app.route("/game/<gameID>/<characterID>/", methods=["GET", "POST"])
@login_required
def game(gameID, characterID):
    print('ENTERING GAME SCREEN')
    game = db.session.query(Game).filter(Game.id == gameID).first()
    flask.session['room'] = str(game.id)
    character = db.session.query(Character).filter(Character.id == characterID).first()
    rolePlayer = db.session.query(Player).filter(Player.gameID == game.id).filter(Player.userID == current_user.id).first()
    
     #TODO: REMOVE
    if(isinstance(rolePlayer, NoneType)):
        return render_template("gameScreen.html", game=game, user=current_user.username, char=character, role=0)
    
    return render_template("gameScreen.html", game=game, user=current_user.username, char=character, role=rolePlayer.role)
#-----------------------------------------------------------------------------------------
#-------------------------------------- LOG OUT ------------------------------------------
#-----------------------------------------------------------------------------------------
@app.get('/logout/')
@login_required
def get_logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('get_login'))
#-----------------------------------------------------------------------------------------
#-------------------------------------- REMOVE GAME --------------------------------------
#-----------------------------------------------------------------------------------------
@app.get('/home/<gameID>')
@login_required
def remove_game(gameID):
    game_to_rmv = Game.query.filter_by(id = gameID).first()
    players_to_rmv = Game.query.filter_by(id = gameID).first().gamers
    
    for item in players_to_rmv:
        db.session.delete(item)
        
    db.session.delete(game_to_rmv)
    db.session.commit()
    return redirect(url_for('home'))
#-----------------------------------------------------------------------------------------
#-------------------------------------- REMOVE CHARACTER ---------------------------------
#-----------------------------------------------------------------------------------------
@app.get('/viewCharacters/<characterID>')
@login_required
def remove_character(characterID):
    char_to_rmv = Character.query.filter_by(id = characterID).first()
    db.session.delete(char_to_rmv)
    db.session.commit()
    return redirect(url_for('viewCharacters'))

#-----------------------------------------------------------------------------------------
#-------------------------------------- API ----------------------------------------------
#-----------------------------------------------------------------------------------------
@app.route("/api/getboard/<gameID>/")
def get_board(gameID):
    gameBoard = db.session.query(Game).filter(Game.id == gameID).first()
    return jsonify(gameBoard.board)

@app.route("/api/addboard/<gameID>/", methods=["POST"])
def set_board(gameID):
    content = str(request.json)
    gameBoard = db.session.query(Game).filter(Game.id == gameID).first()
    gameBoard.board = content
    
    db.session.add(gameBoard)
    db.session.commit()
    db.session.flush()

    return jsonify(gameBoard.board)
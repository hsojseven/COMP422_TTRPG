import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, abort, jsonify


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
    return render_template("home.html")
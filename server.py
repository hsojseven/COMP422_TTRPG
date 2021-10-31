import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, abort, jsonify


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(32)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

dictionary = {
  "comment_count": 3,
  "comments": [
    {
      "text": "first",
      "user": 5558675309,
      "timestamp": "2020-11-17T11:27:19Z"
    },
    {
      "text": "First!",
      "user": 4815162342,
      "timestamp": "2020-11-17T11:27:01Z"
    },
    {
      "text": "awwww....",
      "user": 4815162342,
      "timestamp": "2020-11-17T11:27:38Z"
    }
  ]
}

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/posts/")
def posts():
    return jsonify(dictionary)

@app.route("/comments/", methods=['POST'])
def post_comment():
  comment = request.get_json()
  print(comment)
  return "", 201

from lyrics import *
from db import *
from flask import Flask, render_template, url_for, request, redirect, session, g
#from flask.ext.session import Session

app = Flask(__name__)
app.secret_key = "hi"

DATABASE = 'lyrics.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route("/")
def index():
    connectDatabaseName(get_db())
    return render_template("index.html")

@app.route("/wordSearch", methods=["POST"])
def wordSearch():
    lyricquery = request.form.get("lyricquery")
    songIDs = searchForLyrics(lyricquery)
    if songIDs.size == 0:
        return render_template("none.html")
    return render_template("results.html", list=list)

@app.route("/songSearch", methods=["POST"])
def songSearch():
    songquery = request.form.get("songquery")
    songList = getSongsPlainSearch(songquery)
    session['songList'] = songList
    return render_template("songresults.html", list=songList)

@app.route("/songadd", methods=["POST"])
def songAdd():
    songNumber = request.form.get("songNumber")
    songList = session.get('songList', None)
    runIt(songList, int(songNumber))
    return render_template("addsuccess.html", songNumber=songNumber)

@app.route("/back", methods=["POST"])
def back():
    return redirect(url_for('index'))

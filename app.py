from lyrics import *
from db import *
from flask import Flask, render_template, url_for, request, redirect, session
#from flask.ext.session import Session

app = Flask(__name__)
"""SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)"""
app.secret_key = "hi"

@app.route("/")
def index():
    DATA = db.connectDatabase("lyrics.db")
    session['DB'] = DATA
    return render_template("index.html")

@app.route("/wordSearch", methods=["POST"])
def wordSearch():
    lyricquery = request.form.get("lyricquery")
    songIDs = searchforLyrics(lyricquery)
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

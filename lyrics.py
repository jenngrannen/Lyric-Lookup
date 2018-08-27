import requests
import db
import json
from bs4 import BeautifulSoup

def getUrlLyrics(url):
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c, 'html.parser')
    lyrics = soup.select("body > .main-page > .row > div:nth-of-type(2) > div:nth-of-type(5)")
    return lyrics[0].get_text()

def cleanUpLyrics(lyrics):
    openlist = []
    closedlist = []
    openvalue = 0
    while openvalue != -1:
        openvalue = lyrics.find("[")
        closedvalue = lyrics.find("]")
        lyrics = lyrics.replace(lyrics[openvalue:closedvalue+1], "")
    b = "!@#$.,?%'\"()*&;:+=—_–/"
    lyrics = lyrics.replace("-", " ")
    for char in b:
        lyrics = lyrics.replace(char, "")
    return lyrics.lower()

def createTables():
    #data = db.connectDatabase("lyrics.db")
    db.execute(DATA, "CREATE TABLE names(songID integer PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, artist TEXT NOT NULL, lyrics TEXT NOT NULL)")
    db.execute(DATA, "CREATE TABLE words(word TEXT PRIMARY KEY, songs BLOB NOT NULL)")


def storeSong(title, artist, lyrics):
    lyrics = cleanUpLyrics(lyrics)
    query = 'INSERT INTO names (name, artist, lyrics) VALUES (\"{}\", \"{}\", \"{}\");'.format(title, artist, lyrics)
    db.execute(DATA, query)
    songID = db.execute(DATA, 'SELECT songID FROM names WHERE name = \"{}\" AND artist = \"{}\"'.format(title, artist)).fetchone()
    return songID[0]


def storeLyrics(songID, lyrics):
    lyrics = cleanUpLyrics(lyrics)
    lyricsSplit = lyrics.split()
    lyricsSplit = list(set(lyricsSplit))
    wordsList = db.execute(DATA, 'SELECT word FROM words').fetchall()
    wordsList = [word[0] for word in wordsList]
    for songWord in lyricsSplit:
        if songWord not in wordsList:
            list1 = [songID]
            listString = json.dumps(list1)
            db.execute(DATA, 'INSERT INTO words (word, songs) VALUES (\"{}\", \"{}\")'.format(songWord, listString))
        else:
            list1 = db.execute(DATA, 'SELECT songs FROM words WHERE word = \"{}\"'.format(songWord)).fetchone()[0]
            list2 = json.loads(list1)
            print(list2)
            list2.append(songID)
            list1 = json.dumps(list2)
            db.execute(DATA, 'UPDATE words SET songs = \"{}\" WHERE word = \"{}\"'.format(list1, songWord))

def formatURL(search):
    base = "https://search.azlyrics.com/search.php?q="
    search = search.replace(" ", "+")
    return base + search

def getFiveSongs(url):
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c, 'html.parser')
    song = []
    artist = []
    link = []
    tableCount = soup.select("table")
    tables = len(tableCount)
    if tables == 1:
        j = 1
    else:
        j = 0
    for i in range(5):
        song.append(soup.select("table:nth-of-type({}) tr:nth-of-type({}) > td > a > b".format(tables, i+j+1))[0].get_text())
        artist.append(soup.select("table:nth-of-type({}) tr:nth-of-type({}) > td > b".format(tables, i+j+1))[0].get_text())
        link.append(soup.select("table:nth-of-type({}) tr:nth-of-type({}) > td > a".format(tables, i+j+1))[0]['href'])
    results = [song, artist, link]
    return results

def searchForLyrics(query):
    query = cleanUpLyrics(query)
    querySplit = query.split()
    queryNoRepeat = list(set(querySplit))
    wordsList = db.execute(DATA, 'SELECT word FROM words').fetchall()
    wordsList = [word[0] for word in wordsList]
    for qword in queryNoRepeat:
        if qword not in wordsList:
            return -2
    masterlist = []
    retlist = []
    list1 = db.execute(DATA, 'SELECT songs FROM words WHERE word = \"{}\"'.format(queryNoRepeat[0])).fetchone()[0]
    list2 = json.loads(list1)
    masterlist.extend(list2)
    for qword in queryNoRepeat:
        list1 = db.execute(DATA, 'SELECT songs FROM words WHERE word = \"{}\"'.format(qword)).fetchone()[0]
        list2 = json.loads(list1)
        for songID in masterlist:
            if songID not in list2:
                masterlist.remove(songID)
    for songID in masterlist:
        lyricTemp = db.execute(DATA, 'SELECT lyrics FROM names WHERE songID = {}'.format(songID)).fetchone()[0]
        if query in lyricTemp:
            retlist.append(songID)
    return retlist



DATA = db.connectDatabase("lyrics.db")
def runIt(search, index):
    #testLyrics = getUrlLyrics("https://www.azlyrics.com/lyrics/drake/inmyfeelings.html")
    songTest = getFiveSongs(formatURL(search))
    testLyrics = getUrlLyrics(songTest[2][index-1])
    songID = storeSong(songTest[0][index-1], songTest[1][index-1], testLyrics)
    storeLyrics(songID, testLyrics)
    #lyrics2 = cleanUpLyrics(lyrics)
    #songID = storeSong("In My Feelings", "Drake", lyrics2)
    #storeLyrics(songID, lyrics2)

create = False
if create:
    createTables()
#runIt("do you love me",1)
print(searchForLyrics("something in the water"))

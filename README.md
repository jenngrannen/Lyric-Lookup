# Lyric Lookup

#### Efficiently lookup a lyric for songs in your music library.

Lyric Lookup uses BeautifulSoup to extract song lyrics for your music library from AZLyrics.com, and stores them in a SQLite database. You can then use the Flask interface to look up a song, simply by putting in a string that you'd like to search for.

*Dependencies: Python >3.0, Flask, sqlite3, BeautifulSoup4, requests*

#### Features:
* **Add a song to your library:** Type the name (or a part of the name, more specific the better) of the song you'd like to add to your library of searchable songs. You'll then see a list of top search results (sometimes songs have the same name), from which you can select your song.
* **Search for a lyric from your library:** Input a lyric that you'd like to search in your library of songs. It'll then give you a list of songs that contain your given query.

#### Todo:
* Add Spotify account integration to auto-populate music library
* Add support for accounts for Heroku deployment

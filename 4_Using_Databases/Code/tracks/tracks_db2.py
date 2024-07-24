# same as tracks_db.py (diff in line 91)
from xml.etree import ElementTree
import sqlite3

# <key>Track ID</key><integer>801</integer>
# <key>Name</key><string>These Foolish Things Remind Me Of You</string>
# <key>Artist</key><string>David Osborne</string>
def lookup(children, key):
    keyfound = False
    for child in children:
        if keyfound:
            return child.text
        if child.tag == 'key' and child.text == key:
            keyfound = True
    return None


db_path = 'tracks_db2.sqlite'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;

CREATE TABLE Genre(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Artist(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Album(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    rating INTEGER,
    artist_id INTEGER
);

CREATE TABLE Track(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    rating INTEGER, len INTEGER, count INTEGER, release_year INTEGER,
    album_id INTEGER,
    genre_id INTEGER
);
''')


fpath = 'Library.xml'
etree = ElementTree.parse(fpath)
dict_list = etree.findall('dict/dict/dict')
print(len(dict_list))
count = 1
for contents in dict_list:
    if lookup(contents, 'Track ID') is None:
        continue  # skip dict with no Track # IDEA:
    track_title = lookup(contents, 'Name')
    artist_name = lookup(contents, 'Artist')
    album_title = lookup(contents, 'Album')
    genre_name = lookup(contents, 'Genre')
    track_size = lookup(contents, 'Size')
    track_len = lookup(contents, 'Total Time')
    track_count = lookup(contents, 'Play Count')
    track_releaseyear = lookup(contents, 'Year')
    track_rating = lookup(contents, 'Rating')
    album_rating = lookup(contents, 'Album Rating')

    if genre_name is None or artist_name is None or album_title is None or track_title is None:
        continue

    print(str(count) + '. ' + track_title + ', ' + artist_name + ', ' + album_title + ', ' + genre_name)

    cur.execute("INSERT OR IGNORE INTO Genre(name) VALUES(?)", (genre_name,))
    cur.execute("SELECT id FROM Genre WHERE name = ?", (genre_name,))
    genre_id = cur.fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO Artist(name) VALUES(?)", (artist_name,))
    cur.execute("SELECT id FROM Artist WHERE name = ?", (artist_name,))
    artist_id = cur.fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO Album(title, rating, artist_id) VALUES(?, ?, ?)", (album_title, album_rating, artist_id))
    cur.execute("SELECT id FROM Album WHERE title = ?", (album_title,))
    album_id = cur.fetchone()[0]

    cur.execute("INSERT OR REPLACE INTO Track(title, rating, len, count, release_year, album_id, genre_id) VALUES(?, ?, ?, ?, ?, ?, ?)",
                (track_title, track_rating, track_len, track_count, track_releaseyear, album_id, genre_id))

    conn.commit()
    count += 1
cur.close()
conn.close()
print('All Done!')

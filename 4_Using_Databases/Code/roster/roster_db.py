import json
import sqlite3

conn = sqlite3.connect('roster_db.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;

CREATE TABLE User(
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE,
    email   TEXT UNIQUE
);

CREATE TABLE Course(
    id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title   TEXT UNIQUE
);

CREATE TABLE Member(
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY(user_id, course_id)
);
''')

fpath = 'roster_data.json'
fhand = open(fpath)
str_data = fhand.read()
list_roster = json.loads(str_data)
count = 1
for entry in list_roster:
    user_name = entry[0]
    course_title = entry[1]
    member_role = entry[2]

    print(str(count) + '. ' + user_name + ', ' + course_title + ', ' + str(member_role))

    cur.execute('INSERT OR IGNORE INTO User(name) VALUES(?)', (user_name,))
    cur.execute('SELECT id FROM User WHERE name = ?', (user_name,))
    user_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Course(title) VALUES(?)', (course_title,))
    cur.execute('SELECT id FROM Course WHERE title = ?', (course_title,))
    course_id = cur.fetchone()[0]

    cur.execute('INSERT OR REPLACE INTO Member(user_id, course_id, role) VALUES(?, ?, ?)', (user_id, course_id, member_role))

    conn.commit()
    count += 1
cur.close()
conn.close()

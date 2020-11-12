'''
Will create a simple database in it's directory.
If database already exists, doses nothing.
'''

import sqlite3

# connection to database
mydb = sqlite3.connect("space_journey_db.db")

# create a cursor
my_cursor = mydb.cursor()

# check if there are tables in database
my_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Players'")
content = my_cursor.fetchall()

# if there are no tables, execute
if not content:
    # create tables
    my_cursor.execute("CREATE TABLE Players( player_id INTEGER AUTO_INCREMENT PRIMARY KEY, username VARCHAR(20) NOT NULL, password VARCHAR(20) NOT NULL)")
    my_cursor.execute("CREATE TABLE Scores( score_id INTEGER AUTO_INCREMENT PRIMARY KEY, username VARCHAR(20) NOT NULL, score int(10) NOT NULL)")

# commit our commands
mydb.commit()


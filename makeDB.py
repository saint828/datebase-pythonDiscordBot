import sqlite3
con=sqlite3.connect("charaDB.db")
try:
    con.execute("DROP TABLE if exists chara;")
    con.execute("CREATE TABLE chara (name TEXT,guildID INTEGER,autorID INTEGER,pass TEXT UNIQUE);")
except sqlite3.IntegrityError:
    con.rollback()
finally:
    con.commit()
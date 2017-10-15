import sqlite3 as lite

conn = lite.connect('currentDB')
cur = conn.cursor()

def get_posts():
    cur.execute("SELECT * FROM entries")
    print(cur.fetchall())

get_posts()

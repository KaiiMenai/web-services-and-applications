import sqlite3 # https://docs.python.org/3/library/sqlite3.html; https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders
import dbconfig as cfg
database = cfg.mysql["database"] # https://www.sqlitetutorial.net/sqlite-python/; https://www.sqlitetutorial.net/sqlite-python/insert/

con = sqlite3.connect(database)
cur = con.cursor()
with open("schema.sql", "r") as fp:
    sql = fp.read()

cur.executescript(sql)
con.close()
print("sanity")
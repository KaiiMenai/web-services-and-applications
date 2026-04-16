import sqlite3
import dbconfig as cfg
database = cfg.mysql["database"]

con = sqlite3.connect(database)
cur = con.cursor()
with open("schema.sql", "r") as fp:
    sql = fp.read()

cur.executescript(sql)
con.close()
print("sanity")
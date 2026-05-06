# createschema.py - https://www.sqlitetutorial.net/sqlite-python/creating-database/; https://www.sqlitetutorial.net/sqlite-python/
# This file initialises the SQLite database from schema.sql for the task management application.
# Run this ONCE before starting the server: python createschema.py
# WARNING: This will DROP and recreate ALL tables, deleting existing data.
# author: Kyra Menai Hamilton

import sqlite3 # https://docs.python.org/3/library/sqlite3.html; https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders
import dbconfig as cfg
from os import path

ROOT  = path.dirname(path.realpath(__file__))
database = path.join(ROOT, cfg.mysql["database"]) # https://www.sqlitetutorial.net/sqlite-python/; https://www.sqlitetutorial.net/sqlite-python/insert/

con = sqlite3.connect(database)
cur = con.cursor()
with open(path.join(ROOT, "schema.sql"), "r") as fp:
    sql = fp.read()

cur.executescript(sql)
con.commit()

# Check that the tables were actually created.
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cur.fetchall()]
for table in ['user', 'category', 'task']:
    print(f" {table}: {'OK' if table in tables else ' MISSING'}")

con.close()
print("sanity")
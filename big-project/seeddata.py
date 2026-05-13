# seeddata.py
# This program is used to populate the database with initial data for testing and demonstration purposes/
# Run ONCE after createschema.py: python seeddata.py
# WARNING: This will put demo data into the database. Run createschema.py to  reset the database.
# author: Kyra Menai Hamilton

import sqlite3
from os import path
from werkzeug.security import generate_password_hash  # https://werkzeug.palletsprojects.com/en/stable/utils/#werkzeug.security.generate_password_hash
import dbconfig as cfg

ROOT     = path.dirname(path.realpath(__file__))
database = path.join(ROOT, cfg.mysql['database'])
con      = sqlite3.connect(database)
cur      = con.cursor()

# --- Demo users ---
# Login with these credentials when demoing the app
users = [
    ('alice',   'alice@taskflow.com',   'password123'),
    ('bob',     'bob@taskflow.com',     'password123'),
]

user_ids = {}
for username, email, password in users:
    pw_hash = generate_password_hash(password)
    cur.execute(
        "INSERT INTO user (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, pw_hash)
    )
    user_ids[username] = cur.lastrowid

con.commit()

# --- Categories per user ---
categories = {
    'alice': ['Work', 'Personal', 'Urgent'],
    'bob':   ['Study', 'Home', 'Health'],
}

cat_ids = {}
for username, cat_list in categories.items():
    uid = user_ids[username]
    cat_ids[username] = {}
    for name in cat_list:
        cur.execute(
            "INSERT INTO category (name, user_id) VALUES (?, ?)",
            (name, uid)
        )
        cat_ids[username][name] = cur.lastrowid

con.commit()

# --- Tasks ---
# (task_name, description, due_date, status, category_key, username)
tasks = [
    # Alice's tasks
    ('Finish project report',   'Write up the final section and proofread.',  '2026-05-14', 'in-progress', 'Work',     'alice'),
    ('Team meeting prep',       'Prepare slides for Thursday standup.',        '2026-05-13', 'pending',     'Work',     'alice'),
    ('Book dentist appointment','Check availability for next week.',           '2026-05-20', 'pending',     'Personal', 'alice'),
    ('Renew car insurance',     'Compare quotes online before renewal date.',  '2026-05-10', 'done',        'Urgent',   'alice'),
    ('Fix login bug',           'Users report session expiry too soon.',       '2026-05-12', 'done',        'Work',     'alice'),
    ('Buy birthday present',    'Gift for Mums birthday on the 18th.',        '2026-05-18', 'pending',     'Personal', 'alice'),
    ('Review researcher profiles',      'Assess experience and qualifications of potential researchers.',     '2026-05-13', 'in-progress', 'Work',     'alice'),

    # Bob's tasks
    ('Study for databases exam','Review normalisation and indexing chapters.', '2026-05-16', 'in-progress', 'Study',    'bob'),
    ('Clean the kitchen',       'Deep clean including oven and fridge.',       '2026-05-15', 'pending',     'Home',     'bob'),
    ('Morning run',             '5km run before 8am.',                        '2026-05-13', 'done',        'Health',   'bob'),
    ('Submit assignment',       'WSAA big project - final submission.',        '2026-05-14', 'in-progress', 'Study',    'bob'),
    ('Food shopping',        'Milk, eggs, bread, pizza, and veggies.',  '2026-05-14', 'pending',     'Home',     'bob'),
    ('Doctors checkup',         'Annual health check at 10am.',               '2026-05-21', 'pending',     'Health',   'bob'),
    ('Read book',         'Finish the last chapter.',  '2026-05-13', 'done',        'Study',    'bob'),
]

for task_name, description, due_date, status, category_key, username in tasks:
    uid    = user_ids[username]
    cat_id = cat_ids[username].get(category_key)
    cur.execute(
        "INSERT INTO task (task_name, description, due_date, status, category_id, user_id) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (task_name, description, due_date, status, cat_id, uid)
    )

con.commit()
con.close()

# --- Summary ---
print("\nSeed data inserted successfully.")
print("-" * 40)
print("Demo accounts:")
for username, email, password in users:
    print(f"  username: {username:<10} password: {password}")
print("-" * 40)
print(f"  {len(tasks)} tasks across {len(users)} users")
print()

# END
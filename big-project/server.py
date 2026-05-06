# server.py
# This module sets up a Flask web server to handle HTTP requests for managing tasks. 
# It defines routes for creating, reading, updating, and deleting tasks, and uses the taskDAO and userDAO classes to interact with the database. 
# The server is designed to be simple and easy to extend with additional functionality as needed. 
# author: Kyra Menai Hamilton

from flask import Flask, jsonify, request, abort, redirect, url_for, session # https://help.pythonanywhere.com/pages/Flask/; https://stackoverflow.com/questions/56529391/setting-and-retrieving-environmental-variables-in-flask-applications
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user # https://flask.palletsprojects.com/en/stable/quickstart/#http-methods
import logging
from logging.handlers import RotatingFileHandler
import os
from categoryDAO import categoryDAO
#from flask_cors import CORS, cross_origin
# app = Flask(__name__)
#cors = CORS(app) # allow CORS for all domains on all routes.
#app.config['CORS_HEADERS'] = 'Content-Type'

from taskDAO import taskDAO
from userDAO import userDAO

app = Flask(__name__, static_url_path='', static_folder='.') # https://flask.palletsprojects.com/en/stable/quickstart/; https://flask.palletsprojects.com/en/stable/patterns/packages/
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

bcrypt = Bcrypt(app) # https://flask-bcrypt.readthedocs.io/en/1.0.1/; https://www.freecodecamp.org/news/how-to-setup-user-authentication-in-flask/
login_manager = LoginManager(app)
login_manager.login_view = 'serve_login'

# --- Audit logger setup --- # https://stackoverflow.com/questions/14037975/how-do-i-write-flasks-excellent-debug-log-message-to-a-file-in-production; https://oneuptime.com/blog/post/2026-02-02-flask-logging/view; 
def setup_audit_logger():    # https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler; https://flask.palletsprojects.com/en/stable/logging/
    logger = logging.getLogger('audit')
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('audit.log', maxBytes=1_000_000, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(handler)
    return logger

audit_log = setup_audit_logger()

# --- Flask-Login user class --- # https://flask-login.readthedocs.io/en/latest/; https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
class User(UserMixin):
    def __init__(self, user_dict):
        self.id = user_dict['id']
        self.username = user_dict['username']
        self.email = user_dict['email']

@login_manager.user_loader
def load_user(user_id):
    user_dict = userDAO.findByID(int(user_id))
    if user_dict:
        return User(user_dict)
    return None

# --- Serve HTML pages ---
@app.route('/')
@login_required
def index():
    return app.send_static_file('tasksviewer.html')

@app.route('/login')
def serve_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return app.send_static_file('login.html')

@app.route('/register')
def serve_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return app.send_static_file('register.html')

# --- Auth API routes --- # https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
@app.route('/api/register', methods=['POST'])
def register():
    if not request.json:
        abort(400)
    username = request.json.get('username', '').strip()
    email    = request.json.get('email', '').strip()
    password = request.json.get('password', '')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400 # https://flask.palletsprojects.com/en/stable/api/#flask.json.jsonify
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if userDAO.findByUsername(username):
        return jsonify({'error': 'Username already taken'}), 409
    if userDAO.findByEmail(email):
        return jsonify({'error': 'Email already registered'}), 409

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_id = userDAO.create(username, email, password_hash)
    audit_log.info(f"REGISTER | user_id={new_id} | username={username}")
    return jsonify({'message': 'Account created', 'id': new_id}), 201


@app.route('/api/login', methods=['POST']) # https://developer.mozilla.org/en-US/docs/Glossary/REST; https://flask.palletsprojects.com/en/stable/api/#flask.request
def login():
    if not request.json:
        abort(400)
    username = request.json.get('username', '').strip()
    password = request.json.get('password', '')

    user_dict = userDAO.findByUsername(username)
    if not user_dict or not bcrypt.check_password_hash(user_dict['password_hash'], password):
        audit_log.info(f"LOGIN_FAIL | username={username}")
        return jsonify({'error': 'Invalid username or password'}), 401

    user_obj = User(user_dict)
    login_user(user_obj, remember=True)
    audit_log.info(f"LOGIN | user_id={user_obj.id} | username={username}")
    return jsonify({'message': 'Logged in', 'username': username})


@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    audit_log.info(f"LOGOUT | user_id={current_user.id} | username={current_user.username}")
    logout_user()
    return jsonify({'message': 'Logged out'})


@app.route('/api/me')
@login_required
def me():
    return jsonify({'id': current_user.id, 'username': current_user.username, 'email': current_user.email})


# --- Task API routes (all protected) ---
@app.route('/tasks', methods=['GET'])
@login_required
def getAll():
    results = taskDAO.getAll(current_user.id)
    return jsonify(results)


@app.route('/tasks/<int:id>', methods=['GET'])
@login_required
def findById(id):
    task = taskDAO.findByID(id, current_user.id)
    if not task:
        abort(404)
    return jsonify(task)


@app.route('/tasks', methods=['POST'])
@login_required
def create():
    if not request.json:
        abort(400)
    task = {
        'task_name':   request.json.get('task_name', ''),
        'description': request.json.get('description', ''),
        'due_date':    request.json.get('due_date'),
        'status':      request.json.get('status', 'pending'),
        'category_id': request.json.get('category_id'),
    }
    if not task['task_name']:
        return jsonify({'error': 'task_name is required'}), 400

    added = taskDAO.create(task, current_user.id)
    audit_log.info(f"CREATE_TASK | user_id={current_user.id} | task_id={added['id']} | name={task['task_name']}")
    return jsonify(added), 201


@app.route('/tasks/<int:id>', methods=['PUT'])
@login_required
def update(id):
    existing = taskDAO.findByID(id, current_user.id)
    if not existing:
        abort(404)
    if not request.json:
        abort(400)

    req = request.json
    existing['task_name']   = req.get('task_name',   existing['task_name'])
    existing['description'] = req.get('description', existing['description'])
    existing['due_date']    = req.get('due_date',    existing['due_date'])
    existing['status']      = req.get('status',      existing['status'])
    existing['category_id'] = req.get('category_id', existing['category_id'])

    taskDAO.update(id, existing, current_user.id)
    audit_log.info(f"UPDATE_TASK | user_id={current_user.id} | task_id={id} | name={existing['task_name']}")
    return jsonify(existing)

@app.route('/tasks/<int:id>', methods=['DELETE']) # In theory, this should mean that other users can't delete what they don't have access to, but on previous testing I was able to delete Admin1's task whilst logged in as Admin2. - possible issue somewhere else. 
@login_required
def delete(id):
    existing = taskDAO.findByID(id, current_user.id)
    if not existing:
        abort(404)
    taskDAO.delete(id, current_user.id)
    audit_log.info(f"DELETE_TASK | user_id={current_user.id} | task_id={id}")
    return jsonify({'done': True})


# --- Category API routes ---
@app.route('/categories', methods=['GET'])
@login_required
def getCategories():
    return jsonify(categoryDAO.getAll(current_user.id))


@app.route('/categories', methods=['POST'])
@login_required
def createCategory():
    if not request.json or not request.json.get('name'):
        abort(400)
    name = request.json['name'].strip()
    cat  = categoryDAO.create(name, current_user.id)
    audit_log.info(f"CREATE_CATEGORY | user_id={current_user.id} | name={name}")
    return jsonify(cat), 201


@app.route('/categories/<int:id>', methods=['DELETE'])
@login_required
def deleteCategory(id):
    categoryDAO.delete(id, current_user.id)
    audit_log.info(f"DELETE_CATEGORY | user_id={current_user.id} | category_id={id}")
    return jsonify({'done': True})


if __name__ == '__main__':
    app.run(debug=True)

# OLD CODE BELOW - KEEP FOR REFERENCE
#app = Flask(__name__)

#@app.route('/')
#@cross_origin()
# def index():
#    return "Let's, Do it!"

#curl "http://127.0.0.1:5000/tasks"
# @app.route('/tasks')
#@cross_origin()
# def getAll():
#    #print("in getall")
#    results = taskDAO.getAll()
#    return jsonify(results)

#curl "http://127.0.0.1:5000/tasks/2"
# @app.route('/tasks/<int:id>')
#@cross_origin()
#def findById(id):
#    foundTask = taskDAO.findByID(id)

#    return jsonify(foundTask)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"Task Name\":\"hello\",\"Description\":\"someone\",\"Due Date\":22/05/2026}" http://127.0.0.1:5000/tasks
#@app.route('/tasks', methods=['POST'])
#@cross_origin()
#def create():

#    if not request.json:
#        abort(400)
#    # other checking 
#    task = {
#        "Task Name": request.json['task_name'],
#        "Description": request.json['description'],
#        "Due Date": request.json['due_date'],
#    }
#    addedtask = taskDAO.create(task)
#    return jsonify(addedtask)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Task Name\":\"hello\",\"Description\":\"someone\",\"Due Date\":22/05/2026}" http://127.0.0.1:5000/tasks/1
#@app.route('/tasks/<int:id>', methods=['PUT'])
#@cross_origin()
#def update(id):
#    foundTask = taskDAO.findByID(id)
#    if not foundTask:
#        abort(404)

#    if not request.json:
#        abort(400)
#    reqJson = request.json
#    if 'due_date' in reqJson and type(reqJson['due_date']) is not int:
#        abort(400)

#    if 'task_name' in reqJson:
#        foundTask['task_name'] = reqJson['task_name']
#    if 'description' in reqJson:
#        foundTask['description'] = reqJson['description']
#    if 'due_date' in reqJson:
#        foundTask['due_date'] = reqJson['due_date']
#    taskDAO.update(id,foundTask)
#    return jsonify(foundTask)

#@app.route('/tasks/<int:id>' , methods=['DELETE'])
#@cross_origin()
#def delete(id):
#    taskDAO.delete(id)
#    return jsonify({"done":True})

#if __name__ == '__main__' :
#    app.run(debug= True)
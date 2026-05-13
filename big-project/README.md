# Project - Web Services and Applications

## author: Kyra Menai Hamilton

This folder will contain work for the Web Services and Applications module project.

### Project idea

- Task Tracker
- User only access - [flask-bcrypt](https://www.freecodecamp.org/news/how-to-setup-user-authentication-in-flask/) [2](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login)
- Use SQLite and Flask=SQLAlchemy for the app for visuals and layout
- Intergrate JSON - return JSON from RESTful output/endpoints
- Include categorisation for the tasks
- html style is nice - make sure that this is clear to read and User friendly
- frontend - clear to read task/category layout
- AJAX/fetch  use for API
- Add in a file that automatically saves and catalogues login, create, edit, and delete action in a separate file. This will be an example of an audit file showing editing and modification. [1](https://oneuptime.com/blog/post/2026-02-02-flask-logging/view) [2](https://flask.palletsprojects.com/en/stable/logging/) [3](https://stackoverflow.com/questions/14037975/how-do-i-write-flasks-excellent-debug-log-message-to-a-file-in-production)

## The App

### TaskFlow - Fast Task Tracker

TaskFlow is a Flask and SQLite web application for managing personal tasks with user authentication, task categorisation, and audit logging. Users can register, log in, log out, create, read, update/edit, delete tasks, and organise tasks by category through a clean web interface.

### Features

- User registration and login with password hashing.
- User-specific task management.
- CRUD tasks - Create, Read, Update/Edit, and Delete tasks.
- Task categorisation using a separate category table.
- REST-style JSON endpoints.
- AJAX-based frontend interactions.
- Audit logging for key actions such as a register, login, logout, create, read, update/edit, and delete.
- Clean, responsive interface (hopefully) with a custom HTML and CSS.

### Technology

- Python
- Flask
- Flask-Login
- Flask-Bcrypt
- SQLite
- HTML
- CSS
- JavaScript
- jQuery AJAX

### Project Structure

- `server.py` - Flask app, routes, authentication, and JSON endpoints.
- `taskDAO.py` - database access for tasks.
- `userDAO.py` - database access for users.
- `categoryDAO.py` - database access for categories.
- `createschema.py` - creates the SQLite database tables.
- `schema.sql` - SQL schema for the database.
- `dbconfig.py` - database configuration.
- `tasksviewer.html` - main task management page.
- `login.html` - login page.
- `register.html` - registration page.
- `requirements.txt` - Python dependencies.
- `audit.log` - audit trial file created when the app runs.
- `seeddata.py` - example database containing a mix of 14 tasks, in 3 categories at various stages for 2 users.

### Set Up

#### 1. Clone the Repository

```bash
git clone <your-repo-link>
cd <your-repo-folder>
```

#### 2. Create a virtual environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Create the Database

Run the schema setup script once:

```bash
python createschema.py
```

This will create the SQLite database file and the required tables for users, categories, and tasks.

#### 5. (Optional) load the demo data

This will populate the app with example users. categories, and tasks for demonstration.

```bash
python seeddata.py
```

Skip this step to start with an empty database and register an account.

#### 6. Run the application

```bash
python server.py
```

Open the app in a browser:

- `http://127.0.0.1:5000/register` — create an account.
- `http://127.0.0.1:5000/login` — sign in.
- `http://127.0.0.1:5000/` — use the task tracker after logging in.

### How to use it

1. Register for a new account.
2. Log in with the account username and password.
3. Create categories if needed for task categorisation.
4. Add tasks and assign them to a category.
5. Update/Edit or Delete tasks as required.
6. Log out when done.

### API Endpoints

#### Authentication

- `POST /api/register`
- `POST /api/login`
- `POST /api/logout`
- `GET /api/me`

#### Tasks

- `GET /tasks`
- `GET /tasks/<id>`
- `POST /tasks`
- `PUT /tasks/<id>`
- `DELETE /tasks/<id>`
- `PATCH /tasks/<id>`

#### Categories

- `GET /categories`
- `POST /categories`
- `DELETE /categories/<id>`

### Database Notes

The app uses SQLite and stores the data in the database file defined in `dbconfig.py`.

If you need to reset the database, delete the database file and run:

```bash
python createschema.py
```

### Logging

The application writes an audit trail to `audit.log`. This records:

- registration,
- login attempts,
- logout,
- task creation,
- task updates,
- task deletion,
- category actions.

### Troubleshooting

#### `no such table: user`

This usually means the database wasn't yet created.  
Run:

```bash
python createschema.py
```

before starting the server.

#### Virtual environment activation on Windows

If PowerShell blocks activation scripts, run PowerShell as admin and allow scripts for your user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

#### Date input problems

If due dates don't work correctly, make sure the task form uses:

```html
<input type="date" name="due_date">
```

and that the frontend sends the date as a string in `YYYY-MM-DD` format.

### Deployment

This project is currently designed to run locally.

If you deploy it later, add the hosted link here:

`<deployment link here>`

### Notes

- Ensure `SECRET_KEY` is set correctly for secure sessions.
- Make sure `createschema.py` is run before first use.

#### AI prompt used for the interface

Tool: Claude (claude.ai)

- Explain how I can make a clean user authenticated version with the flask-login and bcrypt.
- I would  like to add the option to have tabs on the left of the main page to choose what to view; tasks by person, task categories, tasks completed. I also want to add that if a task is deleted there needs to be a prompt asking the user to input why. I also want user to have the ability to have a check box that marks tasks as complete. If tasks need to be reopened, then a new task is created linking to the old one

# END
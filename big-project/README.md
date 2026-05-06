# Project - Web Services and Applications

author: Kyra Menai Hamilton

This folder will contain work for the Web Services and Applications module project.

## The App

## Features

## Technology

## Project idea

- Task Tracker
- User only access - [flask-bcrypt](https://www.freecodecamp.org/news/how-to-setup-user-authentication-in-flask/) [2](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login)
- Use SQLite and Flask=SQLAlchemy for the app for visuals and layout
- Intergrate JSON - return JSON from RESTful output/endpoints
- Include categorisation for the tasks
- html style is nice - make sure that this is clear to read and User friendly
- frontend - clear to read task/category layout
- AJAX/fetch  use for API
- Add in a file that automatically saves and catalogues login, create, edit, and delete action in a separate file. This will be an example of an audit file showing editing and modification. [1](https://oneuptime.com/blog/post/2026-02-02-flask-logging/view) [2](https://flask.palletsprojects.com/en/stable/logging/) [3](https://stackoverflow.com/questions/14037975/how-do-i-write-flasks-excellent-debug-log-message-to-a-file-in-production)

## Project Structure

## Set Up

### 1. Repository

### 2. Create a venv

### 3. Install dependencies

### 4. Daytabase

### 5. Run the app

## How to use it

1. Register
2. Log in
3. Create categories
4. Add tasks and assign to a category
5. Edit/Delete tasks as required
6. Log out when done.

## API Endpoints

### Authentication

### Tasks

### Categories

## Database Notes

The app uses SQLite and stores the data in the database file defined in `dbconfig.py`.

If you need to reset the database, delete the database file and run:

```bash
python createschema.py
```

## Logging

The application writes an audit trail to `audit.log`. This records:

- registration,
- login attempts,
- logout,
- task creation,
- task updates,
- task deletion,
- category actions.

## Troubleshooting

### `no such table: user`

This usually means the database wasn't yet created. Run:

```bash
python createschema.py
```

before starting the server.

### Virtual environment activation on Windows

If PowerShell blocks activation scripts, run PowerShell as admin and allow scripts for your user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Date input problems

If due dates don't work correctly, make sure the task form uses:

```html
<input type="date" name="due_date">
```

and that the frontend sends the date as a string in `YYYY-MM-DD` format.

## Deployment

This project is currently designed to run locally.

If you deploy it later, add the hosted link here:

`<deployment link here>`

- Ensure `SECRET_KEY` is set correctly for secure sessions.
- Make sure `createschema.py` is run before first use.
- This repository should contain only this project for submission.

## To do

- make it look pretty as it looks a little basic at the moment

## Known Issues

- Different users are able to delete each others tasks.

# END

# Web Services and Applications
# Final Project
# author: Kyra Menai Hamilton

# This file contains the initial test idea for the project.

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Creating basic task table - this will be the basis for the task management system. It includes fields for title, description, completion status, and creation timestamp. 
# # I wanted to make sure to include as many different types of data as possible, without overcomplicating the table.

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Method to convert Task object to dictionary for JSON response

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "created_at": self.created_at.isoformat(),
        }

# Now to include a simple route to create a new task and return it as JSON. This will test the basic functionality of the Task model and the database connection.

with app.app_context():
    db.create_all()

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks])

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title required"}), 400
    t = Task(title=title)
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    t = Task.query.get_or_404(task_id)
    data = request.get_json() or {}
    if "done" in data:
        t.done = bool(data["done"])
    if "title" in data:
        t.title = data["title"]
    db.session.commit()
    return jsonify(t.to_dict())

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    t = Task.query.get_or_404(task_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"message": "deleted"})

if __name__ == "__main__":
    app.run(debug=True)

# To view the tasks: http://127.0.0.1:5000/tasks

# END
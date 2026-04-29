# Task DAO - Data Access Object for Task management
# This class provides methods to interact with the Task database, including creating, reading, updating, and deleting tasks. It uses SQLite for simplicity and is designed to be used in a Flask application. 
# The methods include error handling and ensure that database connections are properly managed.
# Author: Kyra Menai Hamilton

import sqlite3
import dbconfig as cfg
from os import path


class TaskDAO:
    def __init__(self):
        self.database = cfg.mysql['database']

    def getcursor(self):
        ROOT = path.dirname(path.realpath(__file__))
        self.connection = sqlite3.connect(path.join(ROOT, self.database))
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()

    def getAll(self, user_id):
        cursor = self.getcursor()
        cursor.execute(
            "SELECT t.*, c.name AS category_name FROM task t "
            "LEFT JOIN category c ON t.category_id = c.id "
            "WHERE t.user_id = ? ORDER BY t.due_date ASC",
            (user_id,)
        )
        results = [dict(row) for row in cursor.fetchall()]
        self.closeAll()
        return results

    def findByID(self, task_id, user_id):
        cursor = self.getcursor()
        cursor.execute(
            "SELECT t.*, c.name AS category_name FROM task t "
            "LEFT JOIN category c ON t.category_id = c.id "
            "WHERE t.id = ? AND t.user_id = ?",
            (task_id, user_id)
        )
        result = cursor.fetchone()
        self.closeAll()
        return dict(result) if result else None

    def create(self, task, user_id):
        cursor = self.getcursor()
        cursor.execute(
            "INSERT INTO task (task_name, description, due_date, status, category_id, user_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                task.get('task_name'),
                task.get('description'),
                task.get('due_date'),
                task.get('status', 'pending'),
                task.get('category_id'),
                user_id
            )
        )
        self.connection.commit()
        task['id'] = cursor.lastrowid
        task['user_id'] = user_id
        self.closeAll()
        return task

    def update(self, task_id, task, user_id):
        cursor = self.getcursor()
        cursor.execute(
            "UPDATE task SET task_name=?, description=?, due_date=?, status=?, category_id=? "
            "WHERE id=? AND user_id=?",
            (
                task.get('task_name'),
                task.get('description'),
                task.get('due_date'),
                task.get('status', 'pending'),
                task.get('category_id'),
                task_id,
                user_id
            )
        )
        self.connection.commit()
        self.closeAll()

    def delete(self, task_id, user_id):
        cursor = self.getcursor()
        cursor.execute(
            "DELETE FROM task WHERE id=? AND user_id=?",
            (task_id, user_id)
        )
        self.connection.commit()
        self.closeAll()

taskDAO = TaskDAO()

#END
# userDAO.py 
# This module provides the UserDAO class for managing user data in a database. It includes methods for creating, reading, updating, and deleting user records. The class uses SQLite for simplicity and is designed to be used in a Flask application. 
# The methods include error handling and ensure that database connections are properly managed.
# author: Kyra Menai Hamilton

import sqlite3
import dbconfig as cfg
from os import path

class UserDAO:
    def __init__(self):
        self.database = cfg.mysql['database']

    def getcursor(self):
        ROOT = path.dirname(path.realpath(__file__))
        self.connection = sqlite3.connect(path.join(ROOT, self.database))
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def closeAll(self):
        self.connection.close()
        
    def create(self, username, email, password_hash):
        cursor = self.getcursor()
        sql = "INSERT INTO user (username, email, password_hash) VALUES (?, ?, ?)"
        cursor.execute(sql, (username, email, password_hash))
        self.connection.commit()
        new_id = cursor.lastrowid
        self.closeAll()
        return new_id
    
    def findByUsername(self, username):
        cursor = self.getcursor()
        cursor.execute("SELECT * FROM user WHERE username = ?", (username,))
        result = cursor.fetchone()
        self.closeAll()
        if result:
            return self.convertToDictionary(result)
        return None
    
    def findByEmail(self, email):
        cursor = self.getcursor()
        cursor.execute("SELECT * FROM user WHERE email = ?", (email,))
        result = cursor.fetchone()
        self.closeAll()
        if result:
            return self.convertToDictionary(result)
        return None
    
    def findByID(self, user_id):
        cursor = self.getcursor()
        cursor.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        self.closeAll()
        if result:
            return self.convertToDictionary(result)
        return None

    def convertToDictionary(self, row):
        keys = ['id', 'username', 'email', 'password_hash', 'created_at']
        return dict(zip(keys, row))


userDAO = UserDAO()
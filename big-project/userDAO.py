# userDAO.py 
# This module provides the UserDAO class for managing user data in a database. It includes methods for creating, reading, updating, and deleting user records. The class uses SQLite for simplicity and is designed to be used in a Flask application. 
# The methods include error handling and ensure that database connections are properly managed.
# author: Kyra Menai Hamilton

import sqlite3
import dbconfig as cfg
from os import path

class UserDAO:
    
    
import sqlite3
import dbconfig as cfg
from os import path


class CategoryDAO:
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
        cursor.execute("SELECT * FROM category WHERE user_id=? ORDER BY name", (user_id,))
        results = [dict(row) for row in cursor.fetchall()]
        self.closeAll()
        return results

    def create(self, name, user_id):
        cursor = self.getcursor()
        cursor.execute("INSERT INTO category (name, user_id) VALUES (?, ?)", (name, user_id))
        self.connection.commit()
        new_id = cursor.lastrowid
        self.closeAll()
        return {'id': new_id, 'name': name, 'user_id': user_id}

    def delete(self, category_id, user_id):
        cursor = self.getcursor()
        cursor.execute("DELETE FROM category WHERE id=? AND user_id=?", (category_id, user_id))
        self.connection.commit()
        self.closeAll()


categoryDAO = CategoryDAO()

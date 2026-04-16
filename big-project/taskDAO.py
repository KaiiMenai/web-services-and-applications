# Task DAO - Data Access Object for Task management
# This class provides methods to interact with the Task database, including creating, reading, updating, and deleting tasks. It uses SQLite for simplicity and is designed to be used in a Flask application. 
# The methods include error handling and ensure that database connections are properly managed.
# Author: Kyra Menai Hamilton

import sqlite3
import dbconfig as cfg
from os import path


class TaskDAO:
    connection=""
    cursor =''
    database=   ''
    
    def __init__(self):
        self.database=   cfg.mysql['database']

    def getcursor(self): 
        ROOT = path.dirname(path.realpath(__file__))

        self.connection = sqlite3.connect(path.join(ROOT,self.database))
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        #self.cursor.close()
         
    def getAll(self):
        cursor = self.getcursor()
        sql="select * from task"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            #print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        sql=f"select * from task where id = {id}"
        
        cursor.execute(sql)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def create(self, task):
        cursor = self.getcursor()
        sql=f"insert into task (Task Name, Description, Due Date) values(\"{task.get('Task Name')}\",\"{task.get('Description')}\",{task.get('Due Date')})"
        print(sql)
        cursor.execute(sql)

        self.connection.commit()
        newid = cursor.lastrowid
        task["id"] = newid
        self.closeAll()
        return task


    def update(self, id, task):
        cursor = self.getcursor()
        sql=f"update task set title= \"{task.get('Task Name')}\", description=\"{task.get('Description')}\", due_date={task.get('Due Date')} where id = {id}"
        print(sql)
        cursor.execute(sql)
        self.connection.commit()
        self.closeAll()
        
    def delete(self, id):
        cursor = self.getcursor()
        sql=f"delete from task where id = {id}"
        
        cursor.execute(sql)

        self.connection.commit()
        self.closeAll()
        
        #print("delete done")

    def convertToDictionary(self, resultLine):
        attkeys=['id','title','description', "due_date"]
        task = {}
        currentkey = 0
        for attrib in resultLine:
            task[attkeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return task

        
taskDAO = TaskDAO()

#END
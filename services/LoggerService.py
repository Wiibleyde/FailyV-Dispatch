import sqlite3
import os
import datetime

class LoggerService:
    def __init__(self, filename, debugMode):
        self.filename = "data/" + filename
        self.debugMode = debugMode
        if not os.path.exists("data"):
            os.makedirs("data")
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req0 = "CREATE TABLE IF NOT EXISTS WebLogs (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, action TEXT, date TEXT)"
        req1 = "CREATE TABLE IF NOT EXISTS ErrorLogs (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, action TEXT, date TEXT)"
        req2 = "CREATE TABLE IF NOT EXISTS DebugLogs (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, action TEXT, date TEXT)"
        req3 = "CREATE TABLE IF NOT EXISTS InfoLogs (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, action TEXT, date TEXT)"
        cursor.execute(req0)
        cursor.execute(req1)
        cursor.execute(req2)
        cursor.execute(req3)
        connection.commit()

    def getDate(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def insertWebLog(self,username,action):
        print(f"WebLog: {username} {action}")
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "INSERT INTO WebLogs (username,action,date) VALUES (?,?,?)"
        cursor.execute(req,(username,action,self.getDate()))
        connection.commit()
        connection.close()

    def insertErrorLog(self,username,action):
        print(f"ErrorLog: {username} {action}")
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "INSERT INTO ErrorLogs (username,action,date) VALUES (?,?,?)"
        cursor.execute(req,(username,action,self.getDate()))
        connection.commit()
        connection.close()

    def insertDebugLog(self,username,action):
        if self.debugMode:
            print(f"DebugLog: {username} {action}")
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "INSERT INTO DebugLogs (username,action,date) VALUES (?,?,?)"
        cursor.execute(req,(username,action,self.getDate()))
        connection.commit()
        connection.close()

    def insertInfoLog(self,username,action):
        print(f"InfoLog: {username} {action}")
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "INSERT INTO InfoLogs (username,action,date) VALUES (?,?,?)"
        cursor.execute(req,(username,action,self.getDate()))
        connection.commit()
        connection.close()

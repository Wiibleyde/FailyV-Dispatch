import sqlite3
import os
import hashlib

class AccountService:
    def __init__(self,filename):
        self.filename = "data/" + filename
        if not os.path.exists("data"):
            os.makedirs("data")
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req0 = "CREATE TABLE IF NOT EXISTS Accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)"
        cursor.execute(req0)
        connection.commit()
        connection.close()

    def insertAccount(self,username,password):
        if self.checkIfExist(username):
            return False
        hashPassword = hashlib.sha256(password.encode()).hexdigest()
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "INSERT INTO Accounts (username,password) VALUES (?,?)"
        cursor.execute(req,(username,hashPassword))
        connection.commit()
        connection.close()

    def checkIfExist(self,username):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT * FROM Accounts WHERE username=?"
        cursor.execute(req,(username,))
        result = cursor.fetchone()
        connection.close()
        if result == None:
            return False
        else:
            return True

    def checkAccount(self,username,pasword):
        hashPassword = hashlib.sha256(pasword.encode()).hexdigest()
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT * FROM Accounts WHERE username=? AND password=?"
        cursor.execute(req,(username,hashPassword))
        result = cursor.fetchone()
        connection.close()
        if result == None:
            return False
        else:
            return True
        
    def deleteAccount(self,username):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "DELETE FROM Accounts WHERE username=?"
        cursor.execute(req,(username,))
        connection.commit()
        connection.close()

    def updateAccount(self,id,newUsername,newPassword):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "UPDATE Accounts SET username=?, password=? WHERE id=?"
        cursor.execute(req,(newUsername,newPassword,id))
        connection.commit()
        connection.close()

    def getIdByUsername(self,username):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT id FROM Accounts WHERE username=?"
        cursor.execute(req,(username,))
        result = cursor.fetchone()
        connection.close()
        if result == None:
            return None
        else:
            return result[0]

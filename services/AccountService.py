import sqlite3
import os
import hashlib

class AccountObject:
    def __init__(self,id,username,password,admin):
        self.id = id
        self.username = username
        self.password = password
        self.admin = admin

    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.id

    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password
    
    def getAdmin(self):
        return self.admin

class AccountService:
    def __init__(self,filename):
        self.filename = "data/" + filename
        if not os.path.exists("data"):
            os.makedirs("data")
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req0 = "CREATE TABLE IF NOT EXISTS Accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)"
        req1 = "CREATE TABLE IF NOT EXISTS Admins (id INTEGER PRIMARY KEY AUTOINCREMENT, userId INTEGER, FOREIGN KEY(userId) REFERENCES Accounts(id))"
        cursor.execute(req0)
        cursor.execute(req1)
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

    def deleteAccountById(self,id):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "DELETE FROM Accounts WHERE id=?"
        cursor.execute(req,(id,))
        connection.commit()
        connection.close()

    def updateAccount(self,id,newUsername,newPassword):
        newPassword256 = hashlib.sha256(newPassword.encode()).hexdigest()
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "UPDATE Accounts SET username=?, password=? WHERE id=?"
        cursor.execute(req,(newUsername,newPassword256,id))
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
        
    def getUsernameById(self,id):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT username FROM Accounts WHERE id=?"
        cursor.execute(req,(id,))
        result = cursor.fetchone()
        connection.close()
        if result == None:
            return None
        else:
            return result[0]
        
    def getAccountPassword(self,username):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT password FROM Accounts WHERE username=?"
        cursor.execute(req,(username,))
        result = cursor.fetchone()
        connection.close()
        if result == None:
            return None
        else:
            return result[0]
        
    def getAllAccounts(self):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT * FROM Accounts"
        cursor.execute(req)
        result = cursor.fetchall()
        connection.close()
        if result == None:
            return None
        else:
            return result

    def checkIfAdmin(self,id):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "SELECT * FROM Admins WHERE userId=?"
        cursor.execute(req,(id,))
        result = cursor.fetchone()
        connection.close()
        if result == None:
            return False
        else:
            return True
        
    def unsetAdmin(self,id):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "DELETE FROM Admins WHERE userId=?"
        cursor.execute(req,(id,))
        connection.commit()
        connection.close()
        
    def setAdmin(self,id):
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req = "INSERT INTO Admins (userId) VALUES (?)"
        cursor.execute(req,(id,))
        connection.commit()
        connection.close()
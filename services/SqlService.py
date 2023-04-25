import sqlite3

class SqlService:
    def __init__(self,filename):
        self.filename = filename
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()
        req0 = "CREATE TABLE IF NOT EXISTS Docteurs (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT, grade TEXT, service BOOLEAN, indisponible BOOLEAN)"
        req2 = "CREATE TABLE IF NOT EXISTS Interventions (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, exterieur BOOLEAN)"
        req3 = "CREATE TABLE IF NOT EXISTS Salles (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT)"
        req4 = "CREATE TABLE IF NOT EXISTS InterventionsDocteurs (id INTEGER PRIMARY KEY AUTOINCREMENT, idIntervention INTEGER, idDocteur INTEGER, FOREIGN KEY(idIntervention) REFERENCES Interventions(id), FOREIGN KEY(idDocteur) REFERENCES Docteurs(id))"
        req5 = "CREATE TABLE IF NOT EXISTS SallesDocteurs (id INTEGER PRIMARY KEY AUTOINCREMENT, idSalle INTEGER, idDocteur INTEGER, FOREIGN KEY(idSalle) REFERENCES Salles(id), FOREIGN KEY(idDocteur) REFERENCES Docteurs(id))"
        self.cursor.execute(req0)
        self.cursor.execute(req2)
        self.cursor.execute(req3)
        self.cursor.execute(req4)
        self.cursor.execute(req5)
        self.connection.commit()


    def insertDoc(self, nom, prenom, grade, service, indisponible):
        req = "INSERT INTO Docteurs (nom, prenom, grade, service, indisponible) VALUES (?,?,?,?,?)"
        self.cursor.execute(req, (nom, prenom, grade, service, indisponible))
        self.connection.commit()

    def insertInt(self, nom, exterieur):
        req = "INSERT INTO Interventions (nom, exterieur) VALUES (?,?)"
        self.cursor.execute(req, (nom, exterieur))
        self.connection.commit()

    def insertSalle(self, nom):
        req = "INSERT INTO Salles (nom) VALUES (?)"
        self.cursor.execute(req, (nom,))
        self.connection.commit()

    def insertIntDoc(self, idIntervention, idDocteur):
        req = "INSERT INTO InterventionsDocteurs (idIntervention, idDocteur) VALUES (?,?)"
        self.cursor.execute(req, (idIntervention, idDocteur))
        self.connection.commit()

    def insertSalleDoc(self, idSalle, idDocteur):
        req = "INSERT INTO SallesDocteurs (idSalle, idDocteur) VALUES (?,?)"
        self.cursor.execute(req, (idSalle, idDocteur))
        self.connection.commit()


    def selectDocById(self, id):
        req = "SELECT * FROM Docteurs WHERE id = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchone()
    
    def selectIntById(self, id):
        req = "SELECT * FROM Interventions WHERE id = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchone()
    
    def selectSalleById(self, id):
        req = "SELECT * FROM Salles WHERE id = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchone()
    
    def selectIntDocById(self, id):
        req = "SELECT * FROM InterventionsDocteurs WHERE id = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchone()
    
    def selectIntByDocId(self, id):
        req = "SELECT * FROM InterventionsDocteurs WHERE idDocteur = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchall()
    
    def selectDocByIntId(self, id):
        req = "SELECT * FROM InterventionsDocteurs WHERE idIntervention = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchall()
    
    def selectIntByIntId(self, id):
        req = "SELECT * FROM InterventionsDocteurs WHERE idIntervention = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchall()
    
    def selectDocByIntId(self, id):
        req = "SELECT * FROM InterventionsDocteurs WHERE idIntervention = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchall()
    
    def selectSalleByDocId(self, id):
        req = "SELECT * FROM SallesDocteurs WHERE idDocteur = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchall()
    
    def selectDocBySalleId(self, id):
        req = "SELECT * FROM SallesDocteurs WHERE idSalle = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchall()
    
    def selectSalleDocById(self, id):
        req = "SELECT * FROM SallesDocteurs WHERE id = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchone()
    
    def selectSalleByIntId(self, id):
        req = "SELECT * FROM SallesDocteurs WHERE idSalle = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchall()
    
    def selectIntBySalleId(self, id):
        req = "SELECT * FROM SallesDocteurs WHERE idSalle = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchall()
    


    def selectDoc(self):
        req = "SELECT * FROM Docteurs"
        self.cursor.execute(req)
        return self.cursor.fetchall()
    
    def selectInt(self):
        req = "SELECT * FROM Interventions"
        self.cursor.execute(req)
        return self.cursor.fetchall()
    
    def selectSalle(self):
        req = "SELECT * FROM Salles"
        self.cursor.execute(req)
        return self.cursor.fetchall()
    
    def selectIntDoc(self):
        req = "SELECT * FROM InterventionsDocteurs"
        self.cursor.execute(req)
        return self.cursor.fetchall()
    
    def selectSalleDoc(self):
        req = "SELECT * FROM SallesDocteurs"
        self.cursor.execute(req)
        return self.cursor.fetchall()
    

    def deleteDoc(self, id):
        req = "DELETE FROM Docteurs WHERE id = ?"
        self.cursor.execute(req, (id,))
        self.connection.commit()
        if self.getIntByDocId(id) != []:
            self.updateIntDoc(self.getIntByDocId(id)[0][0], None, None)

    def deleteInt(self, id):
        req = "DELETE FROM Interventions WHERE id = ?"
        self.cursor.execute(req, (id,))
        self.connection.commit()
        if self.getIntByIntId(id) != []:
            self.updateIntDoc(self.getIntByIntId(id)[0][0], None, None)

    def deleteSalle(self, id):
        req = "DELETE FROM Salles WHERE id = ?"
        self.cursor.execute(req, (id,))
        self.connection.commit()
        if self.getSalleBySalleId(id) != []:
            self.updateSalleDoc(self.getSalleBySalleId(id)[0][0], None, None)

    def deleteIntDoc(self, id):
        req = "DELETE FROM InterventionsDocteurs WHERE id = ?"
        self.cursor.execute(req, (id,))
        self.connection.commit()

    def deleteSalleDoc(self, id):
        req = "DELETE FROM SallesDocteurs WHERE id = ?"
        self.cursor.execute(req, (id,))
        self.connection.commit()

    
    def updateDoc(self, id, nom, prenom, grade, service, indisponible):
        req = "UPDATE Docteurs SET nom = ?, prenom = ?, grade = ?, service = ?, indisponible = ? WHERE id = ?"
        self.cursor.execute(req, (nom, prenom, grade, service, indisponible, id))
        self.connection.commit()

    def updateInt(self, id, nom, exterieur):
        req = "UPDATE Interventions SET nom = ?, exterieur = ? WHERE id = ?"
        self.cursor.execute(req, (nom, exterieur, id))
        self.connection.commit()

    def updateSalle(self, id, nom, exterieur):
        req = "UPDATE Salles SET nom = ?, exterieur = ? WHERE id = ?"
        self.cursor.execute(req, (nom, exterieur, id))
        self.connection.commit()

    def updateIntDoc(self, id, idIntervention, idDocteur):
        req = "UPDATE InterventionsDocteurs SET idIntervention = ?, idDocteur = ? WHERE id = ?"
        self.cursor.execute(req, (idIntervention, idDocteur, id))
        self.connection.commit()

    def updateSalleDoc(self, id, idSalle, idDocteur):
        req = "UPDATE SallesDocteurs SET idSalle = ?, idDocteur = ? WHERE id = ?"
        self.cursor.execute(req, (idSalle, idDocteur, id))
        self.connection.commit()

    
    def close(self):
        self.connection.close()


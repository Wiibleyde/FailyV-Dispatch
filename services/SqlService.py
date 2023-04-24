import sqlite3

class SqlService:
    def __init__(self,filename):
        self.filename = filename
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()
        req = "CREATE TABLE IF NOT EXISTS Docteurs (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT, grade TEXT, service BOOLEAN, indisponible BOOLEAN)"
        req2 = "CREATE TABLE IF NOT EXISTS Interventions (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, exterieur BOOLEAN)"
        req3 = "CREATE TABLE IF NOT EXISTS InterventionsDocteurs (id INTEGER PRIMARY KEY AUTOINCREMENT, idIntervention INTEGER, idDocteur INTEGER, FOREIGN KEY(idIntervention) REFERENCES Interventions(id), FOREIGN KEY(idDocteur) REFERENCES Docteurs(id))"
        self.cursor.execute(req)
        self.cursor.execute(req2)
        self.connection.commit()


    def insertDoc(self, nom, prenom, grade, service, indisponible):
        req = "INSERT INTO Docteurs (nom, prenom, grade, service, indisponible) VALUES (?,?,?,?,?)"
        self.cursor.execute(req, (nom, prenom, grade, service, indisponible))
        self.connection.commit()

    def insertInt(self, nom, exterieur):
        req = "INSERT INTO Interventions (nom, exterieur) VALUES (?,?)"
        self.cursor.execute(req, (nom, exterieur))
        self.connection.commit()

    def insertIntDoc(self, idIntervention, idDocteur):
        req = "INSERT INTO InterventionsDocteurs (idIntervention, idDocteur) VALUES (?,?)"
        self.cursor.execute(req, (idIntervention, idDocteur))
        self.connection.commit()


    def selectDocById(self, id):
        req = "SELECT * FROM Docteurs WHERE id = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchone()
    
    def selectIntById(self, id):
        req = "SELECT * FROM Interventions WHERE id = ?"
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

    def selectDoc(self):
        req = "SELECT * FROM Docteurs"
        self.cursor.execute(req)
        return self.cursor.fetchall()
    
    def selectInt(self):
        req = "SELECT * FROM Interventions"
        self.cursor.execute(req)
        return self.cursor.fetchall()
    
    def selectIntDoc(self):
        req = "SELECT * FROM InterventionsDocteurs"
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

    def deleteIntDoc(self, id):
        req = "DELETE FROM InterventionsDocteurs WHERE id = ?"
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

    def updateIntDoc(self, id, idIntervention, idDocteur):
        req = "UPDATE InterventionsDocteurs SET idIntervention = ?, idDocteur = ? WHERE id = ?"
        self.cursor.execute(req, (idIntervention, idDocteur, id))
        self.connection.commit()

    
    def getDocById(self, id):
        req = "SELECT * FROM Docteurs WHERE id = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchone()
    
    def getIntById(self, id):
        req = "SELECT * FROM Interventions WHERE id = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchone()
    
    def getIntDocById(self, id):
        req = "SELECT * FROM InterventionsDocteurs WHERE id = ?"
        self.cursor.execute(req, (id,))
        return self.cursor.fetchone()
    

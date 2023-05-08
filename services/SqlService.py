import sqlite3
import os

class LSMSSqlService:
    def __init__(self,filename):
        self.filename = "data/" + filename
        if not os.path.exists("data"):
            os.makedirs("data")
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req0 = "CREATE TABLE IF NOT EXISTS Docteurs (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT, grade TEXT, service BOOLEAN, indisponible BOOLEAN, inIntervention BOOLEAN, inSalle BOOLEAN)"
        req2 = "CREATE TABLE IF NOT EXISTS Interventions (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, exterieur BOOLEAN)"
        req3 = "CREATE TABLE IF NOT EXISTS Salles (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT)"
        req4 = "CREATE TABLE IF NOT EXISTS InterventionsDocteurs (id INTEGER PRIMARY KEY AUTOINCREMENT, idIntervention INTEGER, idDocteur INTEGER, FOREIGN KEY(idIntervention) REFERENCES Interventions(id), FOREIGN KEY(idDocteur) REFERENCES Docteurs(id))"
        req5 = "CREATE TABLE IF NOT EXISTS SallesDocteurs (id INTEGER PRIMARY KEY AUTOINCREMENT, idSalle INTEGER, idDocteur INTEGER, FOREIGN KEY(idSalle) REFERENCES Salles(id), FOREIGN KEY(idDocteur) REFERENCES Docteurs(id))"
        cursor.execute(req0)
        cursor.execute(req2)
        cursor.execute(req3)
        cursor.execute(req4)
        cursor.execute(req5)
        connection.commit()

    # Insertion functions

    def insertDoc(self, nom, prenom, grade, service, indisponible, inIntervention, inSalle):
        if self.selectDocByNomPrenom(nom, prenom) is not None:
            return
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO Docteurs (nom, prenom, grade, service, indisponible, inIntervention, inSalle) VALUES (?,?,?,?,?,?,?)"
            cursor.execute(req, (nom, prenom, grade, service, indisponible, inIntervention, inSalle))
            connection.commit()

    def insertInt(self, nom, exterieur):
        if self.selectIntByNom(nom) is not None:
            return
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO Interventions (nom, exterieur) VALUES (?,?)"
            cursor.execute(req, (nom, exterieur))
            connection.commit()

    def insertSalle(self, nom):
        if self.selectSalleByNom(nom) is not None:
            return
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO Salles (nom) VALUES (?)"
            cursor.execute(req, (nom,))
            connection.commit()

    def insertIntDoc(self, idIntervention, idDocteur):
        if self.selectIntDocByIntIdDocId(idIntervention, idDocteur) is not None:
            return
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO InterventionsDocteurs (idIntervention, idDocteur) VALUES (?,?)"
            cursor.execute(req, (idIntervention, idDocteur))
            connection.commit()

    def insertSalleDoc(self, idSalle, idDocteur):
        if self.selectSalleDocByDocIdSalleId(idSalle, idDocteur) is not None:
            return
        if self.selectSalleDocByDocId(idDocteur) is not None:
            self.deleteSalleDocByDocId(idDocteur)
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO SallesDocteurs (idSalle, idDocteur) VALUES (?,?)"
            cursor.execute(req, (idSalle, idDocteur))
            connection.commit()

    # Selection functions

    def selectDocById(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Docteurs WHERE id = ?"
            cursor.execute(req, (id,))
            return cursor.fetchone()
        
    def selectDocByNomPrenom(self, nom, prenom):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Docteurs WHERE nom = ? AND prenom = ?"
            cursor.execute(req, (nom, prenom))
            return cursor.fetchone()
        
    def selectIntByNom(self, nom):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Interventions WHERE nom = ?"
            cursor.execute(req, (nom,))
            return cursor.fetchone()
        
    def selectSalleByNom(self, nom):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Salles WHERE nom = ?"
            cursor.execute(req, (nom,))
            return cursor.fetchone()
    
    def selectIntById(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Interventions WHERE id = ?"
            cursor.execute(req, (id,))
            return cursor.fetchone()
    
    def selectSalleById(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Salles WHERE id = ?"
            cursor.execute(req, (id,))
            return cursor.fetchone()
    
    def selectIntDocById(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsDocteurs WHERE id = ?"
            cursor.execute(req, (id,))
            return cursor.fetchone()
        
    def selectIntDocByIntIdDocId(self, idIntervention, idDocteur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsDocteurs WHERE idIntervention = ? AND idDocteur = ?"
            cursor.execute(req, (idIntervention, idDocteur))
            return cursor.fetchone()
    
    def selectSalleByDocId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs WHERE idDocteur = ?"
            cursor.execute(req, (id,))
            return cursor.fetchall()
    
    def selectDocBySalleId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs WHERE idSalle = ?"
            cursor.execute(req, (id,))
            return cursor.fetchall()
    
    def selectSalleDocById(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs WHERE id = ?"
            cursor.execute(req, (id,))
            return cursor.fetchone()
        
    def selectSalleDocByDocId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs WHERE idDocteur = ?"
            cursor.execute(req, (id,))
            return cursor.fetchone()
    
    def selectSalleDocByDocIdSalleId(self, idSalle, idDocteur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs WHERE idSalle = ? AND idDocteur = ?"
            cursor.execute(req, (idSalle, idDocteur))
            return cursor.fetchone()
    
    def selectIntBySalleId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs WHERE idSalle = ?"
            cursor.execute(req, (id,))
            return cursor.fetchall()

    def selectDoc(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Docteurs ORDER BY prenom"
            cursor.execute(req)
            return cursor.fetchall()
    
    def selectInt(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Interventions"
            cursor.execute(req)
            return cursor.fetchall()
    
    def selectSalle(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Salles"
            cursor.execute(req)
            return cursor.fetchall()
    
    def selectIntDoc(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsDocteurs"
            cursor.execute(req)
            return cursor.fetchall()
    
    def selectSalleDoc(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs"
            cursor.execute(req)
            return cursor.fetchall()
    
    # Delete functions

    def deleteDoc(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM Docteurs WHERE id = ?"
            cursor.execute(req, (id,))
            connection.commit()
            self.deleteSalleDocByDocId(id)
            self.deleteIntDocByDocId(id)

    def deleteInt(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM Interventions WHERE id = ?"
            cursor.execute(req, (id,))
            connection.commit()
            if self.selectIntDocByIntIdDocId(id, None) != None:
                self.deleteIntDocByIntId(id)

    def deleteSalle(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM Salles WHERE id = ?"
            cursor.execute(req, (id,))
            connection.commit()

    def deleteIntDoc(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsDocteurs WHERE id = ?"
            cursor.execute(req, (id,))
            connection.commit()

    def deleteIntDocByDocId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsDocteurs WHERE idDocteur = ?"
            cursor.execute(req, (id,))
            connection.commit()
            
    def deleteIntDocByIntId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsDocteurs WHERE idIntervention = ?"
            cursor.execute(req, (id,))
            connection.commit()

    def deleteDocFromInt(self, idDoc, idInt):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsDocteurs WHERE idDocteur = ? AND idIntervention = ?"
            cursor.execute(req, (idDoc, idInt))
            connection.commit()

    def deleteSalleDocByDocId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM SallesDocteurs WHERE idDocteur = ?"
            cursor.execute(req, (id,))
            connection.commit()

    def deleteSalleDoc(self, idDoc, idSalle):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM SallesDocteurs WHERE idDocteur = ? AND idSalle = ?"
            cursor.execute(req, (idDoc, idSalle))
            connection.commit()

    # Update functions
    
    def updateDoc(self, id, nom, prenom, grade, service, indisponible, inIntervention, inSalle):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE Docteurs SET nom = ?, prenom = ?, grade = ?, service = ?, indisponible = ?, inIntervention = ?, inSalle = ? WHERE id = ?"
            cursor.execute(req, (nom, prenom, grade, service, indisponible, inIntervention, inSalle, id))
            connection.commit()

    def updateInt(self, id, nom, exterieur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE Interventions SET nom = ?, exterieur = ? WHERE id = ?"
            cursor.execute(req, (nom, exterieur, id))
            connection.commit()

    def updateSalle(self, id, nom, exterieur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE Salles SET nom = ?, exterieur = ? WHERE id = ?"
            cursor.execute(req, (nom, exterieur, id))
            connection.commit()

    def updateIntDoc(self, id, idIntervention, idDocteur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE InterventionsDocteurs SET idIntervention = ?, idDocteur = ? WHERE id = ?"
            cursor.execute(req, (idIntervention, idDocteur, id))
            connection.commit()

    def updateSalleDoc(self, id, idSalle, idDocteur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE SallesDocteurs SET idSalle = ?, idDocteur = ? WHERE id = ?"
            cursor.execute(req, (idSalle, idDocteur, id))
            connection.commit()

    # Insert functions

    def close(self):
        with sqlite3.connect(self.filename) as connection:
            connection.close()

class LSPDSqlService:
    def __init__(self,filename):
        self.filename = "data/" + filename
        if not os.path.exists("data"):
            os.makedirs("data")
        connection = sqlite3.connect(self.filename)
        cursor = connection.cursor()
        req0 = "CREATE TABLE IF NOT EXISTS Agents (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT, grade TEXT, service BOOLEAN, indisponible BOOLEAN, inIntervention BOOLEAN, inSalle BOOLEAN)"
        req2 = "CREATE TABLE IF NOT EXISTS Interventions (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, exterieur BOOLEAN)"
        req3 = "CREATE TABLE IF NOT EXISTS Salles (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT)"
        req4 = "CREATE TABLE IF NOT EXISTS InterventionsAgents (id INTEGER PRIMARY KEY AUTOINCREMENT, idIntervention INTEGER, idAgent INTEGER, FOREIGN KEY(idIntervention) REFERENCES Interventions(id), FOREIGN KEY(idAgent) REFERENCES Agents(id))"
        req5 = "CREATE TABLE IF NOT EXISTS SallesAgents (id INTEGER PRIMARY KEY AUTOINCREMENT, idSalle INTEGER, idAgent INTEGER, FOREIGN KEY(idSalle) REFERENCES Salles(id), FOREIGN KEY(idAgent) REFERENCES Agents(id))"
        cursor.execute(req0)
        cursor.execute(req2)
        cursor.execute(req3)
        cursor.execute(req4)
        cursor.execute(req5)
        connection.commit()

    # Insertion functions

    def insertAge(self, nom, prenom, grade, service, indisponible, inIntervention, inSalle):
        if self.selectAgeByNomPrenom(nom, prenom) is not None:
            return
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO Agents (nom, prenom, grade, service, indisponible, inIntervention, inSalle) VALUES (?,?,?,?,?,?,?)"
            cursor.execute(req, (nom, prenom, grade, service, indisponible, inIntervention, inSalle))
            connection.commit()

    def insertInt(self, nom, exterieur):
        if self.selectIntByNom(nom) is not None:
            return
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO Interventions (nom, exterieur) VALUES (?,?)"
            cursor.execute(req, (nom, exterieur))
            connection.commit()

    def insertSalle(self, nom):
        if self.selectSalleByNom(nom) is not None:
            return
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO Salles (nom) VALUES (?)"
            cursor.execute(req, (nom,))
            connection.commit()

    def insertIntAge(self, idIntervention, idAgent):
        if self.selectIntAgeByIntIdAgeId(idIntervention, idAgent) is not None:
            return
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO InterventionsAgents (idIntervention, idAgent) VALUES (?,?)"
            cursor.execute(req, (idIntervention, idAgent))
            connection.commit()

    def insertSalleDoc(self, idSalle, idAgent):
        if self.selectSalleAgeByAgeIdSalleId(idSalle, idAgent) is not None:
            return
        if self.selectSalleAgeByAgeId(idAgent) is not None:
            self.deleteSalleAgeByAgeId(idAgent)
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO SallesAgents (idSalle, idAgent) VALUES (?,?)"
            cursor.execute(req, (idSalle, idAgent))
            connection.commit()

    def insertSalleAge(self, idSalle, idAgent):
        if self.selectSalleAgeByAgeIdSalleId(idSalle, idAgent) is not None:
            return
        if self.selectSalleAgeByAgeId(idAgent) is not None:
            self.deleteSalleAgeByAgeId(idAgent)
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO SallesAgents (idSalle, idAgent) VALUES (?,?)"
            cursor.execute(req, (idSalle, idAgent))
            connection.commit()

    # Selection functions

    def selectAgeById(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Agents WHERE id = ?"
            cursor.execute(req, (id,))
            return cursor.fetchone()
        
    def selectAgeByNomPrenom(self, nom, prenom):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Agents WHERE nom = ? AND prenom = ?"
            cursor.execute(req, (nom, prenom))
            return cursor.fetchone()
        
    def selectIntByNom(self, nom):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Interventions WHERE nom = ?"
            cursor.execute(req, (nom,))
            return cursor.fetchone()
        
    def selectSalleByNom(self, nom):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Salles WHERE nom = ?"
            cursor.execute(req, (nom,))
            return cursor.fetchone()
    
    def selectIntById(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Interventions WHERE id = ?"
            cursor.execute(req, (id,))
            return cursor.fetchone()
    
    def selectSalleById(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Salles WHERE id = ?"
            cursor.execute(req, (id,))
            return cursor.fetchone()
    
    def selectIntAgeById(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsAgents WHERE id = ?"
            cursor.execute(req, (id,))
            return cursor.fetchone()
        
    def selectIntAgeByIntIdAgeId(self, idIntervention, idAgent):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsAgents WHERE idIntervention = ? AND idAgent = ?"
            cursor.execute(req, (idIntervention, idAgent))
            return cursor.fetchone()
        
    def selectIntAgeByAgeId(self, idAgent):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsAgents WHERE idAgent = ?"
            cursor.execute(req, (idAgent,))
            return cursor.fetchall()
    
    def selectIntByAgeId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsAgents WHERE idAgent = ?"
            cursor.execute(req, (id,))
            return cursor.fetchall()
    
    def selectSalleByAgeId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesAgents WHERE idAgent = ?"
            cursor.execute(req, (id,))
            return cursor.fetchall()
    
    def selectAgeBySalleId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesAgents WHERE idSalle = ?"
            cursor.execute(req, (id,))
            return cursor.fetchall()
    
    def selectSalleAgeById(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesAgents WHERE id = ?"
            cursor.execute(req, (id,))
            return cursor.fetchone()
        
    def selectSalleAgeByAgeId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesAgents WHERE idAgent = ?"
            cursor.execute(req, (id,))
            return cursor.fetchone()
    
    def selectSalleAgeByAgeIdSalleId(self, idSalle, idAgent):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesAgents WHERE idSalle = ? AND idAgent = ?"
            cursor.execute(req, (idSalle, idAgent))
            return cursor.fetchone()
    
    def selectIntBySalleId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesAgents WHERE idSalle = ?"
            cursor.execute(req, (id,))
            return cursor.fetchall()

    def selectAge(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Agents ORDER BY prenom"
            cursor.execute(req)
            return cursor.fetchall()
    
    def selectInt(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Interventions"
            cursor.execute(req)
            return cursor.fetchall()
    
    def selectSalle(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Salles"
            cursor.execute(req)
            return cursor.fetchall()
    
    def selectIntAge(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsAgents"
            cursor.execute(req)
            return cursor.fetchall()
    
    def selectSalleAge(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesAgents"
            cursor.execute(req)
            return cursor.fetchall()
    
    # Delete functions

    def deleteAge(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM Agents WHERE id = ?"
            cursor.execute(req, (id,))
            connection.commit()
            self.deleteSalleAgeByAgeId(id)
            self.deleteIntAgeByAgeId(id)

    def deleteInt(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM Interventions WHERE id = ?"
            cursor.execute(req, (id,))
            connection.commit()
            if self.selectIntAgeByIntIdAgeId(id, None) != None:
                self.deleteIntAgeByIntId(id)

    def deleteSalle(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM Salles WHERE id = ?"
            cursor.execute(req, (id,))
            connection.commit()

    def deleteIntAge(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsAgents WHERE id = ?"
            cursor.execute(req, (id,))
            connection.commit()

    def deleteIntAgeByAgeId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsAgents WHERE idAgent = ?"
            cursor.execute(req, (id,))
            connection.commit()

    def deleteIntAgeByIntId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsAgents WHERE idIntervention = ?"
            cursor.execute(req, (id,))
            connection.commit()
            
    def deleteAgeFromInt(self, idAge, idInt):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsAgents WHERE idAgent = ? AND idIntervention = ?"
            cursor.execute(req, (idAge, idInt))
            connection.commit()

    def deleteSalleAgeByAgeId(self, id):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM SallesAgents WHERE idAgent = ?"
            cursor.execute(req, (id,))
            connection.commit()

    def deleteSalleAge(self, idAge, idSalle):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM SallesAgents WHERE idAgent = ? AND idSalle = ?"
            cursor.execute(req, (idAge, idSalle))
            connection.commit()

    # Update functions
    
    def updateAge(self, id, nom, prenom, grade, service, indisponible, inIntervention, inSalle):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE Agents SET nom = ?, prenom = ?, grade = ?, service = ?, indisponible = ?, inIntervention = ?, inSalle = ? WHERE id = ?"
            cursor.execute(req, (nom, prenom, grade, service, indisponible, inIntervention, inSalle, id))
            connection.commit()

    def updateInt(self, id, nom, exterieur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE Interventions SET nom = ?, exterieur = ? WHERE id = ?"
            cursor.execute(req, (nom, exterieur, id))
            connection.commit()

    def updateSalle(self, id, nom, exterieur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE Salles SET nom = ?, exterieur = ? WHERE id = ?"
            cursor.execute(req, (nom, exterieur, id))
            connection.commit()

    def updateIntAge(self, id, idIntervention, idAgent):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE InterventionsAgents SET idIntervention = ?, idAgent = ? WHERE id = ?"
            cursor.execute(req, (idIntervention, idAgent, id))
            connection.commit()

    def updateSalleAge(self, id, idSalle, idAgent):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE SallesAgents SET idSalle = ?, idAgent = ? WHERE id = ?"
            cursor.execute(req, (idSalle, idAgent, id))
            connection.commit()

    # Insert functions

    def close(self):
        with sqlite3.connect(self.filename) as connection:
            connection.close()


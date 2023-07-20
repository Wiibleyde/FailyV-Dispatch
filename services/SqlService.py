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

    def selectDocById(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Docteurs WHERE id = ?"
            cursor.execute(req, (iden,))
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
    
    def selectIntById(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Interventions WHERE id = ?"
            cursor.execute(req, (iden,))
            return cursor.fetchone()
    
    def selectSalleById(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Salles WHERE id = ?"
            cursor.execute(req, (iden,))
            return cursor.fetchone()
    
    def selectIntDocById(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsDocteurs WHERE id = ?"
            cursor.execute(req, (iden,))
            return cursor.fetchone()

    def selectDocByIntId(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsDocteurs WHERE idIntervention = ?"
            cursor.execute(req, (iden,))
            return cursor.fetchall()
        
    def selectIntDocByIntIdDocId(self, idIntervention, idDocteur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsDocteurs WHERE idIntervention = ? AND idDocteur = ?"
            cursor.execute(req, (idIntervention, idDocteur))
            return cursor.fetchone()
    
    def selectSalleByDocId(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs WHERE idDocteur = ?"
            cursor.execute(req, (iden,))
            return cursor.fetchall()
    
    def selectDocBySalleId(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs WHERE idSalle = ?"
            cursor.execute(req, (iden,))
            return cursor.fetchall()
    
    def selectSalleDocById(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs WHERE id = ?"
            cursor.execute(req, (iden,))
            return cursor.fetchone()
        
    def selectSalleDocByDocId(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs WHERE idDocteur = ?"
            cursor.execute(req, (iden,))
            return cursor.fetchone()
    
    def selectSalleDocByDocIdSalleId(self, idSalle, idDocteur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs WHERE idSalle = ? AND idDocteur = ?"
            cursor.execute(req, (idSalle, idDocteur))
            return cursor.fetchone()
    
    def selectIntBySalleId(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM SallesDocteurs WHERE idSalle = ?"
            cursor.execute(req, (iden,))
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

    def deleteDoc(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM Docteurs WHERE id = ?"
            cursor.execute(req, (iden,))
            connection.commit()
            # self.deleteSalleDocByDocId(id)
            # self.deleteIntDocByDocId(id)

    def deleteInt(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM Interventions WHERE id = ?"
            cursor.execute(req, (iden,))
            connection.commit()
            if self.selectIntDocByIntIdDocId(iden, None) != None:
                self.deleteIntDocByIntId(id)

    def deleteSalle(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM Salles WHERE id = ?"
            cursor.execute(req, (iden,))
            connection.commit()

    def deleteIntDoc(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsDocteurs WHERE id = ?"
            cursor.execute(req, (iden,))
            connection.commit()

    def deleteIntDocByDocId(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsDocteurs WHERE idDocteur = ?"
            cursor.execute(req, (iden,))
            connection.commit()
            
    def deleteIntDocByIntId(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsDocteurs WHERE idIntervention = ?"
            cursor.execute(req, (iden,))
            connection.commit()

    def deleteDocFromInt(self, idDoc, idInt):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsDocteurs WHERE idDocteur = ? AND idIntervention = ?"
            cursor.execute(req, (idDoc, idInt))
            connection.commit()

    def deleteSalleDocByDocId(self, iden):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM SallesDocteurs WHERE idDocteur = ?"
            cursor.execute(req, (iden,))
            connection.commit()

    def deleteSalleDoc(self, idDoc, idSalle):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM SallesDocteurs WHERE idDocteur = ? AND idSalle = ?"
            cursor.execute(req, (idDoc, idSalle))
            connection.commit()

    # Update functions
    
    def updateDoc(self, iden, nom, prenom, grade, service, indisponible, inIntervention, inSalle):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE Docteurs SET nom = ?, prenom = ?, grade = ?, service = ?, indisponible = ?, inIntervention = ?, inSalle = ? WHERE id = ?"
            cursor.execute(req, (nom, prenom, grade, service, indisponible, inIntervention, inSalle, iden))
            connection.commit()

    def updateInt(self, iden, nom, exterieur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE Interventions SET nom = ?, exterieur = ? WHERE id = ?"
            cursor.execute(req, (nom, exterieur, iden))
            connection.commit()

    def updateSalle(self, iden, nom, exterieur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE Salles SET nom = ?, exterieur = ? WHERE id = ?"
            cursor.execute(req, (nom, exterieur, iden))
            connection.commit()

    def updateIntDoc(self, iden, idIntervention, idDocteur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE InterventionsDocteurs SET idIntervention = ?, idDocteur = ? WHERE id = ?"
            cursor.execute(req, (idIntervention, idDocteur, iden))
            connection.commit()

    def updateSalleDoc(self, iden, idSalle, idDocteur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE SallesDocteurs SET idSalle = ?, idDocteur = ? WHERE id = ?"
            cursor.execute(req, (idSalle, idDocteur, iden))
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
        req0 = "CREATE TABLE IF NOT EXISTS Agents (id INTEGER PRIMARY KEY AUTOINCREMENT, matricule VARCHAR(2), nom TEXT, prenom TEXT, grade TEXT, service BOOLEAN, indisponible BOOLEAN, inIntervention BOOLEAN, inAffiliation BOOLEAN)"
        req2 = "CREATE TABLE IF NOT EXISTS Interventions (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, exterieur BOOLEAN)"
        req3 = "CREATE TABLE IF NOT EXISTS Affiliations (id INTEGER PRIMARY KEY, nom TEXT)"
        req4 = "CREATE TABLE IF NOT EXISTS InterventionsAgents (id INTEGER PRIMARY KEY AUTOINCREMENT, idIntervention INTEGER, idAgent INTEGER, FOREIGN KEY(idIntervention) REFERENCES Interventions(id), FOREIGN KEY(idAgent) REFERENCES Agents(id))"
        req5 = "CREATE TABLE IF NOT EXISTS AffiliationsAgents (id INTEGER PRIMARY KEY AUTOINCREMENT, idAffiliation INTEGER, idAgent INTEGER, FOREIGN KEY(idAffiliation) REFERENCES Affiliations(id), FOREIGN KEY(idAgent) REFERENCES Agents(id))"
        cursor.execute(req0)
        cursor.execute(req2)
        cursor.execute(req3)
        cursor.execute(req4)
        cursor.execute(req5)
        connection.commit()

    # Insertion functions

    def insertAgent(self, matricule, nom, prenom, grade):
        # si Agents.matricule existe déjà, on ne fait rien
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO Agents (matricule, nom, prenom, grade, service, indisponible, inIntervention, inAffiliation) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(req, (matricule, nom, prenom, grade, False, False, False, False))
            connection.commit()
    
    def insertInt(self, nom, exterieur):
        # si Interventions.nom existe déjà, on ne fait rien
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO Interventions (nom, exterieur) VALUES (?, ?)"
            cursor.execute(req, (nom, exterieur))
            connection.commit()

    def insertAff(self, nom):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO Affiliations (nom) VALUES (?)"
            cursor.execute(req, (nom,))
            connection.commit()

    def insertIntAgent(self, idIntervention, idAgent):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO InterventionsAgents (idIntervention, idAgent) VALUES (?, ?)"
            cursor.execute(req, (idIntervention, idAgent))
            connection.commit()

    def insertAffAgent(self, idAffiliation, idAgent):
        # si Affiliation.nom = "Lincoln" ou Marie ou Victor pas d'affiliation sinon affiliation
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "INSERT INTO AffiliationsAgents (idAffiliation, idAgent) VALUES (?, ?)"
            cursor.execute(req, (idAffiliation, idAgent))
            connection.commit()

    # Select functions

    def selectAllAgents(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Agents"
            cursor.execute(req)
            return cursor.fetchall()
        
    def selectAllInterventions(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Interventions"
            cursor.execute(req)
            return cursor.fetchall()
        
    def selectAllAffiliations(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Affiliations"
            cursor.execute(req)
            return cursor.fetchall()
        
    def selectAllInterventionsAgents(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsAgents"
            cursor.execute(req)
            return cursor.fetchall()
        
    def selectAllAffiliationsAgents(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM AffiliationsAgents"
            cursor.execute(req)
            return cursor.fetchall()

    def selectAgeById(self,idAge):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Agents WHERE id = ?"
            cursor.execute(req, (idAge,))
            return cursor.fetchone()
        
    def selectAgentByIdInt(self,idInt):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsAgents WHERE idIntervention = ?"
            cursor.execute(req, (idInt,))
            return cursor.fetchall()
        
    def selectIntById(self,idInt):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Interventions WHERE id = ?"
            cursor.execute(req, (idInt,))
            return cursor.fetchone()
        
    def selectAffById(self,idAff):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Affiliations WHERE id = ?"
            cursor.execute(req, (idAff,))
            return cursor.fetchone()
        
    def selectIntAgentById(self,idIntAge):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsAgents WHERE id = ?"
            cursor.execute(req, (idIntAge,))
            return cursor.fetchone()
        
    def selectIntAgentByIdAgent(self,idAgent):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM InterventionsAgents WHERE idAgent = ?"
            cursor.execute(req, (idAgent,))
            return cursor.fetchone()
        
    def selectAffAgentById(self,idAffAge):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM AffiliationsAgents WHERE id = ?"
            cursor.execute(req, (idAffAge,))
            return cursor.fetchone()
        
    def selectAffAgentByIdAgentIdAff(self,idAgent,idAff):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM AffiliationsAgents WHERE idAgent = ? AND idAffiliation = ?"
            cursor.execute(req, (idAgent,idAff))
            return cursor.fetchone()

        
    def selectAffAgentByIdAff(self,idAff):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM AffiliationsAgents WHERE idAffiliation = ?"
            cursor.execute(req, (idAff,))
            return cursor.fetchall()
        
    def selectAllInterventions(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Interventions"
            cursor.execute(req)
            return cursor.fetchall()
        
    def selectAllAffiliations(self):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "SELECT * FROM Affiliations"
            cursor.execute(req)
            return cursor.fetchall()

    # Delete functions

    def deleteAgent(self, idAge):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM Agents WHERE id = ?"
            cursor.execute(req, (idAge,))
            connection.commit()

    def deleteInt(self, idInt):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM Interventions WHERE id = ?"
            cursor.execute(req, (idInt,))
            connection.commit()

    def deleteAff(self, idAff):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM Affiliations WHERE id = ?"
            cursor.execute(req, (idAff,))
            connection.commit()
            if self.selectAffAgentByIdAgentIdAff(None, idAff) != None:
                self.deleteAffAgentByIdAff(idAff)

    def deleteIntAgent(self, idIntAge):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsAgents WHERE id = ?"
            cursor.execute(req, (idIntAge,))
            connection.commit()

    def deleteIntAgentByIdAgent(self, idAgent):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsAgents WHERE idAgent = ?"
            cursor.execute(req, (idAgent,))
            connection.commit()

    def deleteIntAgentByIdInt(self, idInt):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsAgents WHERE idIntervention = ?"
            cursor.execute(req, (idInt,))
            connection.commit()

    def deleteAgentFromInt(self, idAgent, idInt):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM InterventionsAgents WHERE idAgent = ? AND idIntervention = ?"
            cursor.execute(req, (idAgent, idInt))
            connection.commit()

    def deleteAffAgent(self, idAffAge):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM AffiliationsAgents WHERE id = ?"
            cursor.execute(req, (idAffAge,))
            connection.commit()

    def deleteAgentFromAff(self, idAgent, idAff):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM AffiliationsAgents WHERE idAgent = ? AND idAffiliation = ?"
            cursor.execute(req, (idAgent, idAff))
            connection.commit()

    def deleteAffAgentByIdAgent(self, idAgent):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM AffiliationsAgents WHERE idAgent = ?"
            cursor.execute(req, (idAgent,))
            connection.commit()

    def deleteAffAgentByIdAff(self, idAff):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "DELETE FROM AffiliationsAgents WHERE idAffiliation = ?"
            cursor.execute(req, (idAff,))
            connection.commit()

    # Update functions

    def updateAgent(self,id,matricule,nom,prenom,grade,service,indisponible,inIntervention,inAffiliation):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE Agents SET matricule = ?, nom = ?, prenom = ?, grade = ?, service = ?, indisponible = ?, inIntervention = ?, inAffiliation = ? WHERE id = ?"
            cursor.execute(req, (matricule,nom,prenom,grade,service,indisponible,inIntervention,inAffiliation,id))
            connection.commit()        

    def updateInt(self,id,nom,exterieur):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE Interventions SET nom = ?, exterieur = ? WHERE id = ?"
            cursor.execute(req, (nom,exterieur,id))
            connection.commit()

    def updateAff(self,id,nom):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE Affiliations SET nom = ? WHERE id = ?"
            cursor.execute(req, (nom,id))
            connection.commit()

    def updateIntAgent(self,id,idIntervention,idAgent):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE InterventionsAgents SET idIntervention = ?, idAgent = ? WHERE id = ?"
            cursor.execute(req, (idIntervention,idAgent,id))
            connection.commit()

    def updateAffAgent(self,id,idAffiliation,idAgent):
        with sqlite3.connect(self.filename) as connection:
            cursor = connection.cursor()
            req = "UPDATE AffiliationsAgents SET idAffiliation = ?, idAgent = ? WHERE id = ?"
            cursor.execute(req, (idAffiliation,idAgent,id))
            connection.commit()


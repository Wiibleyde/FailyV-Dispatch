class DocteurObj:
    def __init__(self, idDoc, nom, prenom, grade, service, indispo, inInter, inSalle):
        self.idDoc = idDoc
        self.nom = nom
        self.prenom = prenom
        self.grade = grade
        self.service = service
        self.indispo = indispo
        self.inInter = inInter
        self.inSalle = inSalle

    def __str__(self):
        return self.prenom + " " + self.nom
    
    def __repr__(self):
        return self.prenom + " " + self.nom
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.idDoc
    
    def getNom(self):
        return self.nom
    
    def getPrenom(self):
        return self.prenom
    
    def getGrade(self):
        return self.grade
    
    def getService(self):
        return self.service
    
    def getIndispo(self):
        return self.indispo
    
    def getInInter(self):
        return self.inInter
    
    def getInSalle(self):
        return self.inSalle
    
class AgentObj:
    def __init__(self, idAge, nom, prenom, grade, service, indispo, inInter, inSalle):
        self.idAge = idAge
        self.nom = nom
        self.prenom = prenom
        self.grade = grade
        self.service = service
        self.indispo = indispo
        self.inInter = inInter
        self.inSalle = inSalle

    def __str__(self):
        return self.prenom + " " + self.nom
    
    def __repr__(self):
        return self.prenom + " " + self.nom
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.idAge
    
    def getNom(self):
        return self.nom
    
    def getPrenom(self):
        return self.prenom
    
    def getGrade(self):
        return self.grade
    
    def getService(self):
        return self.service
    
    def getIndispo(self):
        return self.indispo
    
    def getInInter(self):
        return self.inInter
    
    def getInSalle(self):
        return self.inSalle

class InterventionObj:
    def __init__(self, idInt, nom, exterieur):
        self.idInt = idInt
        self.nom = nom
        self.exterieur = exterieur
    
    def __str__(self):
        return self.nom
    
    def __repr__(self):
        return self.nom
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.idInt

    def getNom(self):
        return self.nom
    
    def getExterieur(self):
        return self.exterieur
    
class SalleObj:
    def __init__(self, idSalle, nom):
        self.idSalle = idSalle
        self.nom = nom
    
    def __str__(self):
        return self.nom
    
    def __repr__(self):
        return self.nom
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.idSalle
    
    def getNom(self):
        return self.nom

class InterventionDocteursObj:
    def __init__(self, idIntDoc, idIntervention, idDocteur):
        self.idIntDoc = idIntDoc
        self.idIntervention = idIntervention
        self.idDocteur = idDocteur
        
    def __str__(self):
        return self.idIntervention + " " + self.idDocteur
    
    def __repr__(self):
        return self.idIntervention + " " + self.idDocteur
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.idIntDoc
    
    def getIdIntervention(self):
        return self.idIntervention
    
    def getIdDocteur(self):
        return self.idDocteur
    
class InterventionAgentsObj:
    def __init__(self, idIntAge, idIntervention, idAgent):
        self.idIntAge = idIntAge
        self.idIntervention = idIntervention
        self.idAgent = idAgent
        
    def __str__(self):
        return self.idIntervention + " " + self.idAgent
    
    def __repr__(self):
        return self.idIntervention + " " + self.idAgent
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.idIntAge
    
    def getIdIntervention(self):
        return self.idIntervention
    
    def getIdAgent(self):
        return self.idAgent
    
class SalleDocteurObj:
    def __init__(self, idDocSalle, idSalle, idDocteur):
        self.idDocSalle = idDocSalle
        self.idSalle = idSalle
        self.idDocteur = idDocteur
        
    def __str__(self):
        return self.idSalle + " " + self.idDocteur
    
    def __repr__(self):
        return self.idSalle + " " + self.idDocteur
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.idDocSalle
    
    def getIdSalle(self):
        return self.idSalle
    
    def getIdDocteur(self):
        return self.idDocteur
    
class SalleAgentObj:
    def __init__(self, idSalleAge, idSalle, idAgent):
        self.idSalleAge = idSalleAge
        self.idSalle = idSalle
        self.idAgent = idAgent
        
    def __str__(self):
        return self.idSalle + " " + self.idAgent
    
    def __repr__(self):
        return self.idSalle + " " + self.idAgent
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.idSalleAge
    
    def getIdSalle(self):
        return self.idSalle
    
    def getIdAgent(self):
        return self.idAgent
    
class InjuredTypeObj:
    def __init__(self,UR,UA,Delta):
        self.UR = UR
        self.UA = UA
        self.Delta = Delta

    def __str__(self):
        return self.UR + " " + self.UA + " " + self.Delta
    
    def __repr__(self):
        return self.UR + " " + self.UA + " " + self.Delta
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getUR(self):
        return self.UR
    
    def getUA(self):
        return self.UA
    
    def getDelta(self):
        return self.Delta

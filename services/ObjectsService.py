class DocteurObj:
    def __init__(self, id, nom, prenom, grade, service, indispo, inInter, inSalle):
        self.id = id
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
        return self.id
    
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
    def __init__(self, id, nom, exterieur):
        self.id = id
        self.nom = nom
        self.exterieur = exterieur
    
    def __str__(self):
        return self.nom
    
    def __repr__(self):
        return self.nom
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.id

    def getNom(self):
        return self.nom
    
    def getExterieur(self):
        return self.exterieur
    
class SalleObj:
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom
    
    def __str__(self):
        return self.nom
    
    def __repr__(self):
        return self.nom
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.id
    
    def getNom(self):
        return self.nom

class InterventionDocteursObj:
    def __init__(self, id, idIntervention, idDocteur):
        self.id = id
        self.idIntervention = idIntervention
        self.idDocteur = idDocteur
        
    def __str__(self):
        return self.idIntervention + " " + self.idDocteur
    
    def __repr__(self):
        return self.idIntervention + " " + self.idDocteur
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.id
    
    def getIdIntervention(self):
        return self.idIntervention
    
    def getIdDocteur(self):
        return self.idDocteur
    
class SalleDocteurObj:
    def __init__(self, id, idSalle, idDocteur):
        self.id = id
        self.idSalle = idSalle
        self.idDocteur = idDocteur
        
    def __str__(self):
        return self.idSalle + " " + self.idDocteur
    
    def __repr__(self):
        return self.idSalle + " " + self.idDocteur
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.id
    
    def getIdSalle(self):
        return self.idSalle
    
    def getIdDocteur(self):
        return self.idDocteur
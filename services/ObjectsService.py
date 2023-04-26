class DocteurObj:
    def __init__(self, id, nom, prenom, grade, service, indispo):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.grade = grade
        self.service = service
        self.indispo = indispo

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
    def __init__(self, id, id_intervention, id_docteur):
        self.id = id
        self.id_intervention = id_intervention
        self.id_docteur = id_docteur
        
    def __str__(self):
        return self.id_intervention + " " + self.id_docteur
    
    def __repr__(self):
        return self.id_intervention + " " + self.id_docteur
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.id
    
    def getIdIntervention(self):
        return self.id_intervention
    
    def getIdDocteur(self):
        return self.id_docteur
    
class InterventionSallesObj:
    def __init__(self, id, id_intervention, id_salle):
        self.id = id
        self.id_intervention = id_intervention
        self.id_salle = id_salle
        
    def __str__(self):
        return self.id_intervention + " " + self.id_salle
    
    def __repr__(self):
        return self.id_intervention + " " + self.id_salle
    
    def __getattribute__(self, __name: str):
        return object.__getattribute__(self, __name)
    
    def getId(self):
        return self.id
    
    def getIdIntervention(self):
        return self.id_intervention

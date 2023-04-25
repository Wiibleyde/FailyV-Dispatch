class DocteurObj:
    def __init__(self, id, nom, prenom, grade, service, indispo):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.grade = grade
        self.service = service
        self.indispo = indispo

    def __str__(self):
        return self.nom + " " + self.prenom
    
    def __repr__(self):
        return self.nom + " " + self.prenom
    
class InterventionObj:
    def __init__(self, id, nom, exterieur):
        self.id = id
        self.nom = nom
        self.exterieur = exterieur
    
    def __str__(self):
        return self.nom
    
    def __repr__(self):
        return self.nom
    
class SalleObj:
    def __init__(self, id, nom):
        self.id = id
        self.nom = nom
    
    def __str__(self):
        return self.nom
    
    def __repr__(self):
        return self.nom

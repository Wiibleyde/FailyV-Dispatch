class Specialite:
    def __init__(self, nom):
        self.nom = nom

class Grade:
    def __init__(self, nom):
        self.nom = nom

class SpecialiteSecondaire:
    def __init__(self, nom):
        self.nom = nom

class Hopital:
    def __init__(self, salle):
        self.salle = salle
    
class Helico:
    def __init__(self, niveau):
        self.niveau = niveau

class Status:
    def __init__(self, status):
        self.status = status

class Intervention:
    def __init__(self, name, planBlanc):
        self.name = name
        self.planBlanc = planBlanc

class Docteur:
    def __init__(self, nom, specialite, specialiteSecondaire, hopital, helico, status, Intervention):
        self.nom = nom
        self.specialite = specialite
        self.specialiteSecondaire = specialiteSecondaire
        self.hopital = hopital
        self.helico = helico
        self.status = status
        self.Intervention = Intervention

    def setStatus(self, status):
        self.status = status

    def setSalles(self, salles):
        self.hopital = salles

def createIntervention(name):
    return Intervention(name)
    
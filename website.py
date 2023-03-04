class Specialite:
    def __init__(self, nom):
        self.nom = nom

class Grade:
    def __init__(self, nom):
        self.nom = nom

class SpecialiteSecondaire:
    def __init__(self, nom):
        self.nom = nom

class Salle:
    def __init__(self, salle):
        self.salle = salle
    
class Helico:
    def __init__(self, niveau):
        self.niveau = niveau

class Status:
    def __init__(self, status):
        self.status = status

class Intervention:
    def __init__(self, name):
        self.name = name

class Docteur:
    def __init__(self, nom, specialite, specialiteSecondaire, hopital, helico, status, Intervention):
        self.nom = nom
        self.specialite = specialite
        self.specialiteSecondaire = specialiteSecondaire
        self.hopital = hopital
        self.helico = helico
        self.status = status
        self.Intervention = Intervention

def createSpecialite():
    chirugie = Specialite("Chirurgie")
    psychologie = Specialite("Psychologie")
    inspection = Specialite("Inspection")
    traumatologie = Specialite("Traumatologie")
    return chirugie, psychologie, inspection, traumatologie

def createGrade():
    directeur = Grade("Directeur")
    directeurAdjoint = Grade("Directeur Adjoint")
    chefDeService = Grade("Chef de Service")
    specialiste = Grade("Spécialiste")
    titulaire = Grade("Titulaire")
    resident = Grade("Résident")
    interne = Grade("Interne")
    return directeur, directeurAdjoint, chefDeService, specialiste, titulaire, resident, interne

def createSpecialiteSecondaire():
    stock = SpecialiteSecondaire("Stock")
    communication = SpecialiteSecondaire("Communication")
    secourisme = SpecialiteSecondaire("Secourisme")
    ppa = SpecialiteSecondaire("PPA")
    triage = SpecialiteSecondaire("Triage")
    return stock, communication, secourisme, ppa, triage

def createHelico():
    helico0 = Helico(0)
    helico1 = Helico(1)
    helico2 = Helico(2)
    return helico0, helico1, helico2

def createStatus():
    enService = Status("En Service")
    horsService = Status("Hors Service")
    occupe = Status("Occupé")
    enHelico = Status("En Hélico")
    return enService, horsService, occupe, enHelico

def createSalles():
    harper = Salle("Harper")
    kyle = Salle("Kyle")
    sam = Salle("Sam")
    wilfried = Salle("Wilfried")
    bloc1 = Salle("Bloc 1")
    bloc2 = Salle("Bloc 2")
    bloc3 = Salle("Bloc 3")
    bloc4 = Salle("Bloc 4")
    laboratoire = Salle("Laboratoire")
    bureaux = Salle("Bureaux")
    return harper, kyle, sam, wilfried, bloc1, bloc2, bloc3, bloc4, laboratoire, bureaux

def createIntervention():
    planBlanc = Intervention("Plan Blanc")
    planBleu = Intervention("Plan Bleu")
    return planBlanc, planBleu


if __name__=='__name__':
    chirugie, psychologie, inspection, traumatologie = createSpecialite()
    directeur, directeurAdjoint, chefDeService, specialiste, titulaire, resident, interne = createGrade()
    stock, communication, secourisme, ppa, triage = createSpecialiteSecondaire()
    helico0, helico1, helico2 = createHelico()
    enService, horsService, occupe, enHelico = createStatus()
    harper, kyle, sam, wilfried, bloc1, bloc2, bloc3, bloc4, laboratoire, bureaux = createSalles()
    planBlanc, planBleu = createIntervention()
    
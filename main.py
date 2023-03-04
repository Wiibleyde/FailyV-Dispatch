from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

class Specialite:
    def __init__(self, name):
        self.name = name

class Grade:
    def __init__(self, name, color):
        self.name = name
        self.color = color

class SpecialiteSecondaire:
    def __init__(self, name):
        self.name = name

class Salle:
    def __init__(self, name):
        self.name = name
    
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
    def __init__(self, name, telephone, grade, specialite, specialiteSecondaire,helico, status, salle, intervention):
        self.name = name
        self.telephone = telephone
        self.grade = grade
        self.specialite = specialite
        self.specialiteSecondaire = specialiteSecondaire
        self.helico = helico
        self.status = status
        self.salle = salle
        self.intervention = intervention

def createSpecialite():
    chirugie = Specialite("Chirurgie")
    psychologie = Specialite("Psychologie")
    inspection = Specialite("Inspection")
    traumatologie = Specialite("Traumatologie")
    return chirugie, psychologie, inspection, traumatologie

def createGrade():
    # create grade with tailwind color
    directeur = Grade("Directeur", "bg-red-500")
    directeurAdjoint = Grade("Directeur Adjoint", "bg-red-400")
    chefDeService = Grade("Chef de Service", "bg-orange-400")
    specialiste = Grade("Spécialiste", "bg-blue-800")
    titulaire = Grade("Titulaire", "bg-blue-500")
    resident = Grade("Résident", "bg-blue-400")
    interne = Grade("Interne", "bg-green-500")
    return directeur, directeurAdjoint, chefDeService, specialiste, titulaire, resident, interne

def createSpecialiteSecondaire():
    stocks = SpecialiteSecondaire("stocks")
    communication = SpecialiteSecondaire("Communication")
    secourisme = SpecialiteSecondaire("Secourisme")
    ppa = SpecialiteSecondaire("PPA")
    triage = SpecialiteSecondaire("Triage")
    return stocks, communication, secourisme, ppa, triage

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

def createDocteur():
    vassily = Docteur("Vassily Medved", "555-2023", directeur, [chirugie,inspection,traumatologie], [stocks,secourisme], helico2, None, None, None)

    cletus = Docteur("Cletus Christopoulos", "555-2650", directeurAdjoint, [traumatologie], [communication,secourisme,ppa], helico2, None, None, None)

    douglas = Docteur("Douglas Wade", "555-6440", chefDeService, [chirugie,inspection,traumatologie], [stocks,secourisme], helico2, None, None, None)
    maxime = Docteur("Maxime Cross", "555-7015", chefDeService, [chirugie,inspection], [ppa], helico2, None, None, None)
    shawn = Docteur("Shawn Castillo", "555-6548", chefDeService, [chirugie,inspection,traumatologie], [stocks,communication,ppa], helico2, None, None, None)

    adam = Docteur("Adam McKern", "555-8990", specialiste, [psychologie], [communication], helico2, None, None, None)
    astrid = Docteur("Astrid Vogelstein", "555-2879", specialiste, [chirugie,inspection,traumatologie], [stocks], helico2, None, None, None)
    karl = Docteur("Karl Vogelstein", "555-7476", specialiste, [chirugie,inspection,traumatologie], [stocks], helico2, None, None, None)
    jill = Docteur("Jill Park", "555-8588", specialiste, [psychologie], [stocks,secourisme], helico0, None, None, None)

    lucia = Docteur("Lucia Winston", "555-4769", titulaire, [chirugie], [communication,stocks], helico2, None, None, None)
    victoire = Docteur("Victoire Medved", "555-5299", titulaire, [chirugie], [secourisme], helico0, None, None, None)
    eva = Docteur("Eva Ionadi", "555 3430", titulaire, [chirugie], [], helico1, None, None, None)
    nathan = Docteur("Nathan Prale", "555-5420", titulaire, [psychologie], [stocks,secourisme], helico0, None, None, None)
    samuel = Docteur("Samuel Galopin", "555 2428", titulaire, [], [secourisme], helico2, None, None, None)
    cassie = Docteur("Cassie Montgomery", "555-2190", titulaire, [chirugie,inspection], [communication], helico1, None, None, None)
    ruben = Docteur("Ruben Nielsen", "555-4960", titulaire, [chirugie,inspection], [stocks], helico1, None, None, None)

    thomas = Docteur("Thomas Jewison-Reddington", "555-1129", resident, [chirugie,inspection], [stocks,communication], helico2, None, None, None)
    alios = Docteur("Alios Grindumble", "555-0792", resident, [], [], helico1, None, None, None)
    kyra = Docteur("Kyra Walker", "555-8680", resident, [], [ppa], helico0, None, None, None)
    greg = Docteur("Greg Mouse", "555-9244", resident, [], [], helico1, None, None, None)
    zephyr = Docteur("Zephyr Bias", "555-8341", resident, [], [], helico1, None, None, None)

    victorien = Docteur("Victorien Herve", "555-6365", interne, [], [], helico0, None, None, None)

    return vassily, cletus, douglas, maxime, shawn, adam, astrid, karl, jill, lucia, victoire, eva, nathan, samuel, cassie, ruben, thomas, alios, kyra, greg, zephyr, victorien

@app.route('/index')
def index():
    return render_template('index.html', salles=salles, interventions=interventions, doctors=doctors)


if __name__ == '__main__':
    chirugie, psychologie, inspection, traumatologie = createSpecialite()
    directeur, directeurAdjoint, chefDeService, specialiste, titulaire, resident, interne = createGrade()
    stocks, communication, secourisme, ppa, triage = createSpecialiteSecondaire()
    helico0, helico1, helico2 = createHelico()
    enService, horsService, occupe, enHelico = createStatus()
    harper, kyle, sam, wilfried, bloc1, bloc2, bloc3, bloc4, laboratoire, bureaux = createSalles()
    planBlanc, planBleu = createIntervention()
    vassily, cletus, douglas, maxime, shawn, adam, astrid, karl, jill, lucia, victoire, eva, nathan, samuel, cassie, ruben, thomas, alios, kyra, greg, zephyr, victorien = createDocteur()
    doctors = [vassily, cletus, douglas, maxime, shawn, adam, astrid, karl, jill, lucia, victoire, eva, nathan, samuel, cassie, ruben, thomas, alios, kyra, greg, zephyr, victorien]
    salles = [harper, kyle, sam, wilfried, bloc1, bloc2, bloc3, bloc4, laboratoire, bureaux]
    interventions = [planBlanc, planBleu]
    app.run(debug=True)
    
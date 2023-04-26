from flask import Flask, render_template, redirect, url_for, flash
import re

from utils.flaskForms import AddDocteurForm, AddInterventionForm
from utils.regexUtils import RegexUtils
from services.SqlService import SqlService
from services.ObjectsService import DocteurObj, InterventionObj, SalleObj

def addDoctorsToDatabase(docs):
    for doc in docs:
        database.insertDoc(doc.nom, doc.prenom, doc.grade, doc.service, doc.indispo)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddInterventionForm()
    if form.validate_on_submit():
        nom = form.nomInt.data
        exterieur = form.exterieurInt.data
        database.insertInt(nom, exterieur)
        flash('Intervention ajoutée avec succès !')
        return redirect(url_for('index'))
    doctors = database.selectDoc()
    doctorsObj = []
    directeurs = []
    directeursAdjoint = []
    chefsService = []
    specialistes = []
    titulaire = []
    resident = []
    interne = []
    for doc in doctors:
        doc = DocteurObj(doc[0], doc[1], doc[2], doc[3], doc[4], doc[5])
        doctorsObj.append(doc)
        if doc.grade == "Directeur":
            directeurs.append(doc)
        elif doc.grade == "Directeur Adjoint":
            directeursAdjoint.append(doc)
        elif doc.grade == "Chef de service":
            chefsService.append(doc)
        elif doc.grade == "Spécialiste":
            specialistes.append(doc)
        elif doc.grade == "Titulaire":
            titulaire.append(doc)
        elif doc.grade == "Résident":
            resident.append(doc)
        elif doc.grade == "Interne":
            interne.append(doc)
    interventions = database.selectInt()
    interventionsObj = []
    for int in interventions:
        int = InterventionObj(int[0], int[1], int[2])
        interventionsObj.append(int)
    salles = database.selectSalle()
    sallesObj = []
    for salle in salles:
        salle = SalleObj(salle[0], salle[1])
        sallesObj.append(salle)
    intDocs = database.selectIntDoc()
    intDocsObj = []
    for intDoc in intDocs:
        intDocsObj.append(intDoc)
    salleDocs = database.selectSalleDoc()
    salleDocsObj = []
    for salleDoc in salleDocs:
        salleDocsObj.append(salleDoc)
    return render_template('index.html', form=form, interventions=interventionsObj, salles=sallesObj, doctors=doctorsObj, directeurs=directeurs, directeursAdjoints=directeursAdjoint, chefsServices=chefsService, specialistes=specialistes, titulaires=titulaire, residents=resident, internes=interne, intDocs=intDocsObj, salleDocs=salleDocsObj)

@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    form = AddDocteurForm()
    if form.validate_on_submit():
        nom = form.nomDoc.data
        prenom = form.prenomDoc.data
        grade = form.gradeDoc.data
        database.insertDoc(nom, prenom, grade)
        flash('Docteur ajouté avec succès !')
        return redirect(url_for('doctors'))
    doctors = database.selectDocs()
    for doc in doctors:
        doc = DocteurObj(doc[0], doc[1], doc[2], doc[3], doc[4], doc[5])
    return render_template('doctors.html', form=form, doctors=doctors)

@app.route('/setDoctorService/<int:id>', methods=['GET', 'POST'])
def setDoctorServer(id):
    doc = database.selectDocById(id)
    database.updateDoc(id, doc[1], doc[2], doc[3], True, doc[5])
    return redirect(url_for('index'))

@app.route('/unsetDoctorService/<int:id>', methods=['GET', 'POST'])
def unsetDoctorServer(id):
    doc = database.selectDocById(id)
    database.updateDoc(id, doc[1], doc[2], doc[3], False, False)
    return redirect(url_for('index'))

@app.route('/setDoctorIndispo/<int:id>', methods=['GET', 'POST'])
def setDoctorIndispo(id):
    doc = database.selectDocById(id)
    database.updateDoc(id, doc[1], doc[2], doc[3], doc[4], True)
    return redirect(url_for('index'))

@app.route('/unsetDoctorIndispo/<int:id>', methods=['GET', 'POST'])
def unsetDoctorIndispo(id):
    doc = database.selectDocById(id)
    database.updateDoc(id, doc[1], doc[2], doc[3], doc[4], False)
    return redirect(url_for('index'))

@app.route('/setDoctor/<int:idDoc>/toSalle/<string:idSalle>', methods=['GET', 'POST'])
def setDoctorToSalle(idDoc, idSalle):
    doc = database.selectDocById(idDoc)
    database.insertSalleDoc(idDoc, idSalle)
    return redirect(url_for('index'))

@app.route('/unsetDoctor/<int:idDoc>/fromSalle/<string:idSalle>', methods=['GET', 'POST'])
def unsetDoctorFromSalle(idDoc, idSalle):
    database.deleteSalleDoc(idDoc, idSalle)
    return redirect(url_for('index'))

@app.route('/setDoctor/<int:idDoc>/toIntervention/<int:idInt>', methods=['GET', 'POST'])
def setDoctorToIntervention(idDoc, idInt):
    doc = database.selectDocById(idDoc)
    database.insertIntDoc(idInt, idDoc)
    return redirect(url_for('index'))

@app.route('/unsetDoctor/<int:idDoc>/fromIntervention/<int:idInt>', methods=['GET', 'POST'])
def unsetDoctorFromIntervention(idDoc, idInt):
    database.deleteIntDoc(idInt, idDoc)
    return redirect(url_for('index'))

if __name__=='__main__':
    database = SqlService('database.db')
    docs = RegexUtils.doctorToList("""29/06/2021 - 555-2023 Vassily Medved""","Directeur")
    addDoctorsToDatabase(docs)
    docs = RegexUtils.doctorToList("""14/09/2021 - 555-2650 Cletus Christopoulos""","Directeur Adjoint")
    addDoctorsToDatabase(docs)
    docs = RegexUtils.doctorToList("""24/03/2022 - 555-6440 Douglas Wade
        05/02/2021 - 555-7015 Maxime Cross
        26/07/2022 - 555-6548 Shawn Castillo""","Chef de service")
    addDoctorsToDatabase(docs)
    docs = RegexUtils.doctorToList("""14/07/2022 - 555-8990 Adam McKern
        03/08/2022 - 555-2879 Astrid Vogelstein
        21/10/2022 - 555-7476 Karl Vogelstein
        16/07/2022 - 555-4769 Lucia Winston
        27/10/2022 - 555-5299 Victoire Medved
        12/11/2022 - 555-3430 Eva Ionadi""","Spécialiste")
    addDoctorsToDatabase(docs)
    docs = RegexUtils.doctorToList("""09/11/2022 - 555-5420 Nathan Prale
        13/11/2022 - 555-2428 Samuel Galopin
        07/01/2023 - 555-2190 Cassie Montgomery
        23/11/2022 - 555-4960 Ruben Nielsen
        19/11/2022 - 555-8680 Kyra Walker
        19/12/2022 - 555-1129 Thomas Jewison-Reddington""","Titulaire")
    addDoctorsToDatabase(docs)
    docs = RegexUtils.doctorToList("""29/11/2022 - 555-9244 Greg Mouse 
        07/01/2023 - 555-6365 Victorien Herve 
        17/03/2023 - 555-1201 Alvaro Gomez Ortega
        31/03/2023 - 555-3425 Cecil Madera""","Résident")
    addDoctorsToDatabase(docs)
    docs = RegexUtils.doctorToList("""04/04/2023 - 555-0271 Elliot Hawkins
        19/04/2023 - 555-7330 Williams Guster
        21/04/2023 - 555-1412 Emma Vandamme 
        ""","Interne")
    addDoctorsToDatabase(docs)
    database.insertSalle("Harper")
    database.insertSalle("Kyle")
    database.insertSalle("Sam")
    database.insertSalle("Wilfrid")
    database.insertSalle("Bloc 1")
    database.insertSalle("Bloc 2")
    database.insertSalle("Bloc 3")
    database.insertSalle("Bloc 4")
    app.run(debug=True)
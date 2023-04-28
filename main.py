from flask import Flask, render_template, redirect, url_for, flash
import re

from utils.flaskForms import AddDocteurForm, AddInterventionForm
from utils.regexUtils import RegexUtils
from services.SqlService import SqlService
from services.ObjectsService import DocteurObj, InterventionObj, SalleObj, InterventionDocteursObj

def addDoctorsToDatabase(docs):
    for doc in docs:
        database.insertDoc(doc.nom, doc.prenom, doc.grade, doc.service, doc.indispo, doc.inInter, doc.inSalle)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddInterventionForm()
    if form.validate_on_submit():
        nom = form.nomInt.data
        exterieur = form.exterieurInt.data
        database.insertInt(nom, exterieur)
        flash(f'Intervention {nom} ajoutée avec succès !', 'success')
        return redirect(url_for('index'))
    doctors = database.selectDoc()
    doctorsObj = []
    enService = []
    horsService = []
    for doc in doctors:
        inInter = False
        inSalle = False
        if doc[6] == 1:
            inInter = True
        if doc[7] == 1:
            inSalle = True
        doc = DocteurObj(doc[0], doc[1], doc[2], doc[3], doc[4], doc[5], inInter, inSalle)
        doctorsObj.append(doc)
        if doc.service:
            enService.append(doc)
        else:
            horsService.append(doc)
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
        intDoc = InterventionDocteursObj(intDoc[0], intDoc[1], intDoc[2])
        intDocsObj.append(intDoc)
    salleDocs = database.selectSalleDoc()
    salleDocsObj = []
    for salleDoc in salleDocs:
        salleDoc = InterventionDocteursObj(salleDoc[0], salleDoc[1], salleDoc[2])
        salleDocsObj.append(salleDoc)
    return render_template('index.html', form=form, interventions=interventionsObj, salles=sallesObj, doctors=doctorsObj, intDocs=intDocsObj, salleDocs=salleDocsObj, enService=enService, horsService=horsService)

@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    form = AddDocteurForm()
    if form.validate_on_submit():
        nom = form.nomDoc.data
        prenom = form.prenomDoc.data
        grade = form.gradeDoc.data
        database.insertDoc(nom, prenom, grade)
        flash(f'{prenom} ajouté avec succès !', 'success')
        return redirect(url_for('doctors'))
    doctors = database.selectDocs()
    for doc in doctors:
        doc = DocteurObj(doc[0], doc[1], doc[2], doc[3], doc[4], doc[5])
    return render_template('doctors.html', form=form, doctors=doctors)

@app.route('/deleteIntervention/<int:id>', methods=['GET', 'POST'])
def deleteIntervention(id):
    inter = database.selectIntById(id)
    database.deleteInt(id)
    flash(f'{inter[1]} supprimée avec succès !', 'success')
    return redirect(url_for('index'))

@app.route('/setDoctorService/<int:id>', methods=['GET', 'POST'])
def setDoctorServer(id):
    doc = database.selectDocById(id)
    database.updateDoc(id, doc[1], doc[2], doc[3], True, doc[5], doc[6], doc[7])
    flash(f'{doc[2]} {doc[1]} ajouté au service avec succès !', 'success')
    return redirect(url_for('index'))

@app.route('/unsetDoctorService/<int:id>', methods=['GET', 'POST'])
def unsetDoctorServer(id):
    doc = database.selectDocById(id)
    database.updateDoc(id, doc[1], doc[2], doc[3], False, False, doc[6], doc[7])
    flash(f'{doc[2]} {doc[1]} retiré du service avec succès !', 'success')
    return redirect(url_for('index'))

@app.route('/setDoctorIndispo/<int:id>', methods=['GET', 'POST'])
def setDoctorIndispo(id):
    doc = database.selectDocById(id)
    database.updateDoc(id, doc[1], doc[2], doc[3], doc[4], True, doc[6], doc[7])
    flash(f"{doc[2]} {doc[1]} mis en indisponibilité avec succès !", 'success')
    return redirect(url_for('index'))

@app.route('/unsetDoctorIndispo/<int:id>', methods=['GET', 'POST'])
def unsetDoctorIndispo(id):
    doc = database.selectDocById(id)
    database.updateDoc(id, doc[1], doc[2], doc[3], doc[4], False)
    flash(f"{doc[2]} {doc[1]} retiré de l\'indisponibilité avec succès !", 'success')
    return redirect(url_for('index'))

@app.route('/setDoctor/<int:idDoc>/toSalle/<string:idSalle>', methods=['GET', 'POST'])
def setDoctorToSalle(idDoc, idSalle):
    database.insertSalleDoc(idSalle, idDoc)
    doc = database.selectDocById(idDoc)
    database.updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], doc[6], True)
    flash(f'{doc[2]} {doc[1]} ajouté à la salle avec succès !', 'success')
    return redirect(url_for('index'))

@app.route('/unsetDoctor/<int:idDoc>/fromSalle/<string:idSalle>', methods=['GET', 'POST'])
def unsetDoctorFromSalle(idDoc, idSalle):
    database.deleteSalleDoc(idDoc, idSalle)
    doc = database.selectDocById(idDoc)
    database.updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], doc[6], False)
    flash(f'{doc[2]} {doc[1]} retiré de la salle avec succès !', 'success')
    return redirect(url_for('index'))

@app.route('/setDoctor/<int:idDoc>/toIntervention/<int:idInt>', methods=['GET', 'POST'])
def setDoctorToIntervention(idDoc, idInt):
    database.insertIntDoc(idInt, idDoc)
    doc = database.selectDocById(idDoc)
    database.updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], True, doc[7])
    inter = database.selectIntById(idInt)
    flash(f'{doc[2]} {doc[1]} ajouté à l\'intervention {inter[1]} avec succès !', 'success')
    return redirect(url_for('index'))

@app.route('/unsetDoctor/<int:idDoc>/fromIntervention/<int:idInt>', methods=['GET', 'POST'])
def unsetDoctorFromIntervention(idDoc, idInt):
    database.deleteDocFromInt(idDoc, idInt)
    doc = database.selectDocById(idDoc)
    database.updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], False, doc[7])
    inter = database.selectIntById(idInt)
    flash(f'{doc[2]} {doc[1]} retiré de l\'intervention {inter[1]} avec succès !', 'success')
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
    app.run(port=9123,host='0.0.0.0')
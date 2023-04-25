from flask import Flask, render_template, redirect, url_for, flash

from utils.flaskForms import AddDocteurForm, AddInterventionForm
from services.SqlService import SqlService
from services.ObjectsService import DocteurObj, InterventionObj, SalleObj

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = AddInterventionForm()
    if form.validate_on_submit():
        nom = form.nomInt.data
        exterieur = form.exterieurInt.data
        database.insertInt(nom, exterieur)
        flash('Intervention ajoutée avec succès !')
        return redirect(url_for('index'))
    doctors = database.selectDocs()
    for doc in doctors:
        doc = DocteurObj(doc[0], doc[1], doc[2], doc[3], doc[4], doc[5])
    interventions = database.selectInts()
    for int in interventions:
        int = InterventionObj(int[0], int[1], int[2])
    salles = database.selectSalles()
    for salle in salles:
        salle = SalleObj(salle[0], salle[1])
    return render_template('index.html', form=form, doctors=doctors, interventions=interventions, salles=salles)

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

@app.route('/addDocToInt?idInt=<idInt>&docId=<docId>')
def addDocToInt(idInt, docId):
    database.insertIntDoc(idInt, docId)
    intervention = database.selectIntById(idInt)
    flash(f"Docteur ajouté à l'intervention {intervention[1]} avec succès !")
    return redirect(url_for('index'))

@app.route('/addDocToSalle?idSalle=<idSalle>&docId=<docId>')
def addDocToSalle(idSalle, docId):
    database.insertSalleDoc(idSalle, docId)
    salle = database.selectSalleById(idSalle)
    flash(f"Docteur ajouté à la salle {salle[1]} avec succès !")
    return redirect(url_for('index'))

@app.route('/setService?docId=<docId>')
def setService(docId):
    doc = database.selectDocById(docId)
    database.updateDoc(docId, doc[1], doc[2], doc[3], True, doc[5])
    flash(f"Prise du service de {doc[1]} {doc[2]} avec succès !")
    return redirect(url_for('doctors'))

@app.route('/unsetService?docId=<docId>')
def unsetService(docId):
    doc = database.selectDocById(docId)
    database.updateDoc(docId, doc[1], doc[2], doc[3], False, doc[5])
    flash(f"Fin du service de {doc[1]} {doc[2]} avec succès !")
    return redirect(url_for('index'))

@app.route('/setIndispo?docId=<docId>')
def setIndispo(docId):
    doc = database.selectDocById(docId)
    database.updateDoc(docId, doc[1], doc[2], doc[3], doc[4], True)
    flash(f"{doc[1]} {doc[2]} est maintenant indisponible !")
    return redirect(url_for('index'))

@app.route('/unsetIndispo?docId=<docId>')
def unsetIndispo(docId):
    doc = database.selectDocById(docId)
    database.updateDoc(docId, doc[1], doc[2], doc[3], doc[4], False)
    flash(f"{doc[1]} {doc[2]} est maintenant disponible !")
    return redirect(url_for('index'))

if __name__=='__main__':
    database = SqlService('database.db')
    app.run(debug=True)
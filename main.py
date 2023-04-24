from flask import Flask, render_template, redirect, url_for, flash

from utils.flaskForms import AddDocteurForm, AddInterventionForm
from services.SqlService import SqlService

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
    return render_template('index.html')

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
    return render_template('doctors.html', form=form, doctors=database.selectDoc())

@app.route('/addDocToInt?idInt=<idInt>&docId=<docId>')
def addDocToInt(idInt, docId):
    database.insertIntDoc(idInt, docId)
    flash("Docteur ajouté à l'intervention avec succès !")
    return redirect(url_for('interventions'))

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
    return redirect(url_for('doctors'))

@app.route('/setIndispo?docId=<docId>')
def setIndispo(docId):
    doc = database.selectDocById(docId)
    database.updateDoc(docId, doc[1], doc[2], doc[3], doc[4], True)
    flash(f"{doc[1]} {doc[2]} est maintenant indisponible !")
    return redirect(url_for('doctors'))

@app.route('/unsetIndispo?docId=<docId>')
def unsetIndispo(docId):
    doc = database.selectDocById(docId)
    database.updateDoc(docId, doc[1], doc[2], doc[3], doc[4], False)
    flash(f"{doc[1]} {doc[2]} est maintenant disponible !")
    return redirect(url_for('doctors'))

if __name__=='__main__':
    database = SqlService()
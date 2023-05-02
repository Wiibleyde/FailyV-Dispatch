from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import argparse

from services.flaskForms import AddDocteurForm, AddInterventionForm, AddSalleForm, LoginForm, RegisterForm
from services.regexFunc import RegexUtils
from services.SqlService import SqlService
from services.ObjectsService import DocteurObj, InterventionObj, SalleObj, InterventionDocteursObj
from services.AccountService import AccountService

# ======================================================================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
login_manager = LoginManager()
login_manager.init_app(app)
# ======================================================================================================================

class User(UserMixin):
    def __init__(self, id=None):
        self.id = id
    
    def get_id(self):
        return self.id

def addDoctorsToDatabase(userId,docs):
    for doc in docs:
        SqlService(f"{userId}.db").insertDoc(doc.nom, doc.prenom, doc.grade, doc.service, doc.indispo, doc.inInter, doc.inSalle)

def sortDocsByGrade(docs):
    orderGrade = ["Directeur", "Directeur Adjoint", "Chef de service", "Spécialiste", "Titulaire", "Résident", "Interne"]
    docs.sort(key=lambda x: orderGrade.index(x.grade))

def readArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="Run in debug mode", action="store_true")
    parser.add_argument("-p", "--port", help="Port to run on", type=int)
    args = parser.parse_args()
    return args

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.passwordRegister.data != form.confirmPasswordRegister.data:
            flash('Passwords do not match', 'danger')
        elif accounts.checkIfExist(form.usernameRegister.data):
            flash('Username already exists', 'danger')
        else:
            accounts.insertAccount(form.usernameRegister.data, form.passwordRegister.data)
            flash('Account created successfully', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if accounts.checkAccount(form.usernameLogin.data, form.passwordLogin.data):
            user = User(form.usernameLogin.data)
            user.id = form.usernameLogin.data
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = AddInterventionForm()
    if form.validate_on_submit():
        nom = form.nomInt.data
        exterieur = form.exterieurInt.data
        SqlService(f"{current_user.id}.db").insertInt(nom, exterieur)
        flash(f'Intervention {nom} ajoutée avec succès !', 'success')
        return redirect(url_for('index'))
    doctors = SqlService(f"{current_user.id}.db").selectDoc()
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
    sortDocsByGrade(doctorsObj)
    for doc in doctorsObj:
        if doc.service:
            enService.append(doc)
        else:
            horsService.append(doc)
    interventions = SqlService(f"{current_user.id}.db").selectInt()
    interventionsObj = []
    for int in interventions:
        int = InterventionObj(int[0], int[1], int[2])
        interventionsObj.append(int)
    salles = SqlService(f"{current_user.id}.db").selectSalle()
    sallesObj = []
    for salle in salles:
        salle = SalleObj(salle[0], salle[1])
        sallesObj.append(salle)
    intDocs = SqlService(f"{current_user.id}.db").selectIntDoc()
    intDocsObj = []
    for intDoc in intDocs:
        intDoc = InterventionDocteursObj(intDoc[0], intDoc[1], intDoc[2])
        intDocsObj.append(intDoc)
    salleDocs = SqlService(f"{current_user.id}.db").selectSalleDoc()
    salleDocsObj = []
    for salleDoc in salleDocs:
        salleDoc = InterventionDocteursObj(salleDoc[0], salleDoc[1], salleDoc[2])
        salleDocsObj.append(salleDoc)
    return render_template('index.html', form=form, interventions=interventionsObj, salles=sallesObj, doctors=doctorsObj, intDocs=intDocsObj, salleDocs=salleDocsObj, enService=enService, horsService=horsService)

@app.route('/doctors', methods=['GET', 'POST'])
@login_required
def doctors():
    form = AddDocteurForm()
    if form.validate_on_submit():
        doc = RegexUtils.doctorToList(form.zoneText.data, form.grade.data)
        if len(doc) == 0:
            doc = RegexUtils.doctorToString(form.zoneText.data, form.grade.data)
            if doc == None:
                flash(f'Veuillez entrer docteur valide ([Prénom] [Nom]) !', 'danger')
                return redirect(url_for('doctors'))
            else:
                SqlService(f"{current_user.id}.db").insertDoc(doc.nom, doc.prenom, doc.grade, doc.service, doc.indispo, doc.inInter, doc.inSalle)
                flash(f'{doc.prenom} {doc.nom} ajouté avec succès !', 'success')
                return redirect(url_for('doctors'))
        else:
            addDoctorsToDatabase(current_user.id, doc)
            strDoc = ''
            for d in doc:
                strDoc += f'{d.prenom} {d.nom}, '
            flash(f'{strDoc} ajoutés avec succès !', 'success')
            return redirect(url_for('doctors'))
    doctors = SqlService(f"{current_user.id}.db").selectDoc()
    doctorsObj = []
    for doc in doctors:
        doc = DocteurObj(*doc)
        doctorsObj.append(doc)
    sortDocsByGrade(doctorsObj)
    return render_template('doctors.html', form=form, doctors=doctorsObj)

@app.route('/salles', methods=['GET', 'POST'])
@login_required
def salles():
    form = AddSalleForm()
    if form.validate_on_submit():
        nom = form.nomSalle.data
        SqlService(f"{current_user.id}.db").insertSalle(nom)
        flash(f'Salle {nom} ajoutée avec succès !', 'success')
        return redirect(url_for('salles'))
    salles = SqlService(f"{current_user.id}.db").selectSalle()
    sallesObj = []
    for salle in salles:
        salle = SalleObj(salle[0], salle[1])
        sallesObj.append(salle)
    return render_template('salles.html', form=form, salles=sallesObj)

@app.route('/doctor/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteDoctor(id):
    doc = SqlService(f"{current_user.id}.db").selectDocById(id)
    SqlService(f"{current_user.id}.db").deleteDoc(id)
    flash(f'{doc[2]} {doc[1]} supprimé avec succès !', 'success')
    return redirect(url_for('doctors'))

@app.route('/salle/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteSalle(id):
    salle = SqlService(f"{current_user.id}.db").selectSalleById(id)
    SqlService(f"{current_user.id}.db").deleteSalle(id)
    flash(f'{salle[1]} supprimée avec succès !', 'success')
    return redirect(url_for('salles'))

@app.route('/deleteIntervention/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteIntervention(id):
    inter = SqlService(f"{current_user.id}.db").selectIntById(id)
    SqlService(f"{current_user.id}.db").deleteInt(id)
    flash(f'{inter[1]} supprimée avec succès !', 'success')
    return redirect(url_for('index'))

@app.route('/setDoctorService/<int:id>', methods=['GET', 'POST'])
@login_required
def setDoctorServer(id):
    doc = SqlService(f"{current_user.id}.db").selectDocById(id)
    SqlService(f"{current_user.id}.db").updateDoc(id, doc[1], doc[2], doc[3], True, doc[5], doc[6], doc[7])
    flash(f'{doc[2]} {doc[1]} ajouté au service avec succès !', 'success')
    return redirect(url_for('index'))

@app.route('/unsetDoctorService/<int:id>', methods=['GET', 'POST'])
@login_required
def unsetDoctorServer(id):
    doc = SqlService(f"{current_user.id}.db").selectDocById(id)
    SqlService(f"{current_user.id}.db").updateDoc(id, doc[1], doc[2], doc[3], False, False, False, False)
    SqlService(f"{current_user.id}.db").deleteIntDocByDocId(id)
    SqlService(f"{current_user.id}.db").deleteSalleDocByDocId(id)
    flash(f'{doc[2]} {doc[1]} retiré du service avec succès !', 'success')
    return redirect(url_for('index'))

@app.route('/setDoctorIndispo/<int:id>', methods=['GET', 'POST'])
@login_required
def setDoctorIndispo(id):
    doc = SqlService(f"{current_user.id}.db").selectDocById(id)
    SqlService(f"{current_user.id}.db").updateDoc(id, doc[1], doc[2], doc[3], doc[4], True, doc[6], doc[7])
    flash(f"{doc[2]} {doc[1]} mis en indisponibilité avec succès !", 'success')
    return redirect(url_for('index'))

@app.route('/unsetDoctorIndispo/<int:id>', methods=['GET', 'POST'])
@login_required
def unsetDoctorIndispo(id):
    doc = SqlService(f"{current_user.id}.db").selectDocById(id)
    SqlService(f"{current_user.id}.db").updateDoc(id, doc[1], doc[2], doc[3], doc[4], False, doc[6], doc[7])
    flash(f"{doc[2]} {doc[1]} retiré de l\'indisponibilité avec succès !", 'success')
    return redirect(url_for('index'))

@app.route('/setDoctor/<int:idDoc>/toSalle/<string:idSalle>', methods=['GET', 'POST'])
@login_required
def setDoctorToSalle(idDoc, idSalle):
    SqlService(f"{current_user.id}.db").insertSalleDoc(idSalle, idDoc)
    doc = SqlService(f"{current_user.id}.db").selectDocById(idDoc)
    SqlService(f"{current_user.id}.db").updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], doc[6], True)
    flash(f'{doc[2]} {doc[1]} ajouté à la salle avec succès !', 'success')
    return redirect(url_for('index'))

@app.route('/unsetDoctor/<int:idDoc>/fromSalle/<string:idSalle>', methods=['GET', 'POST'])
@login_required
def unsetDoctorFromSalle(idDoc, idSalle):
    SqlService(f"{current_user.id}.db").deleteSalleDoc(idDoc, idSalle)
    doc = SqlService(f"{current_user.id}.db").selectDocById(idDoc)
    SqlService(f"{current_user.id}.db").updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], doc[6], False)
    flash(f'{doc[2]} {doc[1]} retiré de la salle avec succès !', 'success')
    return redirect(url_for('index'))

@app.route('/setDoctor/<int:idDoc>/toIntervention/<int:idInt>', methods=['GET', 'POST'])
@login_required
def setDoctorToIntervention(idDoc, idInt):
    SqlService(f"{current_user.id}.db").insertIntDoc(idInt, idDoc)
    doc = SqlService(f"{current_user.id}.db").selectDocById(idDoc)
    SqlService(f"{current_user.id}.db").updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], True, doc[7])
    inter = SqlService(f"{current_user.id}.db").selectIntById(idInt)
    flash(f'{doc[2]} {doc[1]} ajouté à l\'intervention {inter[1]} avec succès !', 'success')
    return redirect(url_for('index'))

@app.route('/unsetDoctor/<int:idDoc>/fromIntervention/<int:idInt>', methods=['GET', 'POST'])
@login_required
def unsetDoctorFromIntervention(idDoc, idInt):
    SqlService(f"{current_user.id}.db").deleteDocFromInt(idDoc, idInt)
    doc = SqlService(f"{current_user.id}.db").selectDocById(idDoc)
    SqlService(f"{current_user.id}.db").updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], False, doc[7])
    inter = SqlService(f"{current_user.id}.db").selectIntById(idInt)
    flash(f'{doc[2]} {doc[1]} retiré de l\'intervention {inter[1]} avec succès !', 'success')
    return redirect(url_for('index'))

if __name__=='__main__':
    args = readArgs()
    port = 9123
    if args.port != None:
        port = args.port
    accounts = AccountService("accounts.db")
    app.run(port=port,host='0.0.0.0', debug=args.debug)
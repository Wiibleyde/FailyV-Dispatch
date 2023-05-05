from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import argparse

from services.flaskForms import AddLsmsForm, AddLspdForm ,AddInterventionForm, AddSalleForm, LoginForm, RegisterForm
from services.regexFunc import RegexUtils
from services.SqlService import LSMSSqlService, LSPDSqlService
from services.ObjectsService import DocteurObj, AgentObj, InterventionObj, SalleObj, InterventionDocteursObj, InterventionAgentsObj
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
        LSMSSqlService(f"{userId}.db").insertDoc(doc.nom, doc.prenom, doc.grade, doc.service, doc.indispo, doc.inInter, doc.inSalle)

def addAgentsToDatabase(userId,agents):
    for agent in agents:
        LSPDSqlService(f"{userId}.db").insertAgent(agent.nom, agent.prenom, agent.grade, agent.indispo, agent.inIntervention)

def sortDocsByGrade(docs):
    orderGrade = ["Directeur", "Directeur Adjoint", "Chef de service", "Spécialiste", "Titulaire", "Résident", "Interne"]
    docs.sort(key=lambda x: orderGrade.index(x.grade))

def sortAgentsByGrade(agents):
    orderGrade = ["Commissaire", "Capitaine", "Lieutenant", "Inspecteur", "Sergent Chef", "Sergent", "Officier Supérieur", "Officier", "Cadet"]
    agents.sort(key=lambda x: orderGrade.index(x.grade))

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
    flash('Vous devez être connecté pour accèder à cette page !', 'danger')
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    flash("Page introuvable, si vous estimez que cela n'est pas normal, contactez l'administrateur.", 'danger')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.passwordRegister.data != form.confirmPasswordRegister.data:
            flash('Les mots de passe sont différents.', 'danger')
        elif accounts.checkIfExist(form.usernameRegister.data):
            flash("Un compte avec le même nom d'utilisateur existe déjà.", 'danger')
        else:
            accounts.insertAccount(form.usernameRegister.data, form.passwordRegister.data)
            flash('Compte enregistré !', 'success')
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
            flash("Mauvais nom d'utilisateur ou mot de passe.", 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous êtes déconnecté.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/lsms/dispatch', methods=['GET', 'POST'])
@login_required
def lsmsDispatch():
    form = AddInterventionForm()
    if form.validate_on_submit():
        nom = form.nomInt.data
        exterieur = form.exterieurInt.data
        LSMSSqlService(f"{current_user.id}-lsms.db").insertInt(nom, exterieur)
        flash(f'Intervention {nom} ajoutée avec succès !', 'success')
        return redirect(url_for('lsmsDispatch'))
    doctors = LSMSSqlService(f"{current_user.id}-lsms.db").selectDoc()
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
    interventions = LSMSSqlService(f"{current_user.id}-lsms.db").selectInt()
    interventionsObj = []
    for int in interventions:
        int = InterventionObj(int[0], int[1], int[2])
        interventionsObj.append(int)
    salles = LSMSSqlService(f"{current_user.id}-lsms.db").selectSalle()
    sallesObj = []
    for salle in salles:
        salle = SalleObj(salle[0], salle[1])
        sallesObj.append(salle)
    intDocs = LSMSSqlService(f"{current_user.id}-lsms.db").selectIntDoc()
    intDocsObj = []
    for intDoc in intDocs:
        intDoc = InterventionDocteursObj(intDoc[0], intDoc[1], intDoc[2])
        intDocsObj.append(intDoc)
    salleDocs = LSMSSqlService(f"{current_user.id}-lsms.db").selectSalleDoc()
    salleDocsObj = []
    for salleDoc in salleDocs:
        salleDoc = InterventionDocteursObj(salleDoc[0], salleDoc[1], salleDoc[2])
        salleDocsObj.append(salleDoc)
    return render_template('lsms/dispatch.html', form=form, interventions=interventionsObj, salles=sallesObj, doctors=doctorsObj, intDocs=intDocsObj, salleDocs=salleDocsObj, enService=enService, horsService=horsService)

@app.route('/lspd/dispatch', methods=['GET', 'POST'])
@login_required
def lspdDispatch():
    form = AddInterventionForm()
    if form.validate_on_submit():
        nom = form.nomInt.data
        exterieur = form.exterieurInt.data
        LSPDSqlService(f"{current_user.id}-lspd.db").insertInt(nom, exterieur)
        flash(f'Intervention {nom} ajoutée avec succès !', 'success')
        return redirect(url_for('lspdDispatch'))
    agents = LSPDSqlService(f"{current_user.id}-lspd.db").selectAge()
    agentsObj = []
    enService = []
    horsService = []
    for agent in agents:
        inInter = False
        inSalle = False
        if agent[6] == 1:
            inInter = True
        if agent[7] == 1:
            inSalle = True
        agent = AgentObj(agent[0], agent[1], agent[2], agent[3], agent[4], agent[5], inInter, inSalle)
        agentsObj.append(agent)
    sortAgentsByGrade(agentsObj)
    for agent in agentsObj:
        if agent.service:
            enService.append(agent)
        else:
            horsService.append(agent)
    interventions = LSPDSqlService(f"{current_user.id}-lspd.db").selectInt()
    interventionsObj = []
    for int in interventions:
        int = InterventionObj(int[0], int[1], int[2])
        interventionsObj.append(int)
    salles = LSPDSqlService(f"{current_user.id}-lspd.db").selectSalle()
    sallesObj = []
    for salle in salles:
        salle = SalleObj(salle[0], salle[1])
        sallesObj.append(salle)
    intAgents = LSPDSqlService(f"{current_user.id}-lspd.db").selectIntAge()
    intAgentsObj = []
    for intAgent in intAgents:
        intAgent = InterventionAgentsObj(intAgent[0], intAgent[1], intAgent[2])
        intAgentsObj.append(intAgent)
    salleAgents = LSPDSqlService(f"{current_user.id}-lspd.db").selectSalleAge()
    salleAgentsObj = []
    for salleAgent in salleAgents:
        salleAgent = InterventionAgentsObj(salleAgent[0], salleAgent[1], salleAgent[2])
        salleAgentsObj.append(salleAgent)
    return render_template('lspd/dispatch.html', form=form, interventions=interventionsObj, salles=sallesObj, agents=agentsObj, intAgents=intAgentsObj, salleAgents=salleAgentsObj, enService=enService, horsService=horsService)

@app.route('/lsms/doctors', methods=['GET', 'POST'])
@login_required
def lsmsDoctors():
    form = AddLsmsForm()
    if form.validate_on_submit():
        doc = RegexUtils.doctorToList(form.zoneText.data, form.grade.data)
        if len(doc) == 0:
            doc = RegexUtils.doctorToString(form.zoneText.data, form.grade.data)
            if doc == None:
                flash(f'Veuillez entrer docteur valide ([Prénom] [Nom]) !', 'danger')
                return redirect(url_for('lsmsDoctors'))
            else:
                LSMSSqlService(f"{current_user.id}-lsms.db").insertDoc(doc.nom, doc.prenom, doc.grade, doc.service, doc.indispo, doc.inInter, doc.inSalle)
                flash(f'{doc.prenom} {doc.nom} ajouté avec succès !', 'success')
                return redirect(url_for('lsmsDoctors'))
        else:
            addDoctorsToDatabase(current_user.id, doc)
            strDoc = ''
            for d in doc:
                strDoc += f'{d.prenom} {d.nom}, '
            flash(f'{strDoc} ajoutés avec succès !', 'success')
            return redirect(url_for('lsmsDoctors'))
    doctors = LSMSSqlService(f"{current_user.id}-lsms.db").selectDoc()
    doctorsObj = []
    for doc in doctors:
        doc = DocteurObj(*doc)
        doctorsObj.append(doc)
    sortDocsByGrade(doctorsObj)
    return render_template('lsms/doctors.html', form=form, doctors=doctorsObj)

@app.route('/lspd/agents', methods=['GET', 'POST'])
@login_required
def lspdAgents():
    form = AddLspdForm()
    if form.validate_on_submit():
        agent = RegexUtils.agentToList(form.zoneText.data, form.grade.data)
        if len(agent) == 0:
            agent = RegexUtils.agentToString(form.zoneText.data, form.grade.data)
            if agent == None:
                flash(f'Veuillez entrer agent valide ([Prénom] [Nom]) !', 'danger')
                return redirect(url_for('lspdAgents'))
            else:
                LSPDSqlService(f"{current_user.id}-lspd.db").insertAge(agent.nom, agent.prenom, agent.grade, agent.service, agent.indispo, agent.inInter, agent.inSalle)
                flash(f'{agent.prenom} {agent.nom} ajouté avec succès !', 'success')
                return redirect(url_for('lspdAgents'))
        else:
            addAgentsToDatabase(current_user.id, agent)
            strAgent = ''
            for a in agent:
                strAgent += f'{a.prenom} {a.nom}, '
            flash(f'{strAgent} ajoutés avec succès !', 'success')
            return redirect(url_for('lspdAgents'))
    agents = LSPDSqlService(f"{current_user.id}-lspd.db").selectAge()
    agentsObj = []
    for agent in agents:
        agent = AgentObj(*agent)
        agentsObj.append(agent)
    sortAgentsByGrade(agentsObj)
    return render_template('lspd/agents.html', form=form, agents=agentsObj)

@app.route('/lsms/salles', methods=['GET', 'POST'])
@login_required
def lsmsSalles():
    form = AddSalleForm()
    if form.validate_on_submit():
        nom = form.nomSalle.data
        LSMSSqlService(f"{current_user.id}-lsms.db").insertSalle(nom)
        flash(f'Salle {nom} ajoutée avec succès !', 'success')
        return redirect(url_for('lsmsSalles'))
    salles = LSMSSqlService(f"{current_user.id}-lsms.db").selectSalle()
    sallesObj = []
    for salle in salles:
        salle = SalleObj(salle[0], salle[1])
        sallesObj.append(salle)
    return render_template('lsms/salles.html', form=form, salles=sallesObj)

@app.route('/lspd/salles', methods=['GET', 'POST'])
@login_required
def lspdSalles():
    form = AddSalleForm()
    if form.validate_on_submit():
        nom = form.nomSalle.data
        LSPDSqlService(f"{current_user.id}-lspd.db").insertSalle(nom)
        flash(f'Salle {nom} ajoutée avec succès !', 'success')
        return redirect(url_for('lspdSalles'))
    salles = LSPDSqlService(f"{current_user.id}-lspd.db").selectSalle()
    sallesObj = []
    for salle in salles:
        salle = SalleObj(salle[0], salle[1])
        sallesObj.append(salle)
    return render_template('lspd/salles.html', form=form, salles=sallesObj)

@app.route('/lsms/doctor/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsDeleteDoctor(id):
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteDoc(id)
    flash(f'{doc[2]} {doc[1]} supprimé avec succès !', 'success')
    return redirect(url_for('lsmsDoctors'))

@app.route('/lspd/agent/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdDeleteAgent(id):
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteAge(id)
    flash(f'{agent[2]} {agent[1]} supprimé avec succès !', 'success')
    return redirect(url_for('lspdAgents'))

@app.route('/lsms/salle/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsDeleteSalle(id):
    salle = LSMSSqlService(f"{current_user.id}-lsms.db").selectSalleById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteSalle(id)
    flash(f'{salle[1]} supprimée avec succès !', 'success')
    return redirect(url_for('lsmsSalles'))

@app.route('/lspd/salle/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdDeleteSalle(id):
    salle = LSPDSqlService(f"{current_user.id}-lspd.db").selectSalleById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteSalle(id)
    flash(f'{salle[1]} supprimée avec succès !', 'success')
    return redirect(url_for('lspdSalles'))

@app.route('/lsms/deleteIntervention/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsDeleteIntervention(id):
    inter = LSMSSqlService(f"{current_user.id}-lsms.db").selectIntById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteInt(id)
    flash(f'{inter[1]} supprimée avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/deleteIntervention/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdDeleteIntervention(id):
    inter = LSPDSqlService(f"{current_user.id}-lspd.db").selectIntById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteInt(id)
    flash(f'{inter[1]} supprimée avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/setDoctorService/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsSetDoctorServer(id):
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(id, doc[1], doc[2], doc[3], True, doc[5], doc[6], doc[7])
    flash(f'{doc[2]} {doc[1]} ajouté au service avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/setAgentService/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdSetAgentServer(id):
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAge(id, agent[1], agent[2], agent[3], True, agent[5], agent[6], agent[7])
    flash(f'{agent[2]} {agent[1]} ajouté au service avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/unsetDoctorService/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsUnsetDoctorServer(id):
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(id, doc[1], doc[2], doc[3], False, False, False, False)
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteIntDocByDocId(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteSalleDocByDocId(id)
    flash(f'{doc[2]} {doc[1]} retiré du service avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/unsetAgentService/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdUnsetAgentServer(id):
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAge(id, agent[1], agent[2], agent[3], False, False, False, False)
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteIntAgeByAgeId(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteSalleAgeByAgeId(id)
    flash(f'{agent[2]} {agent[1]} retiré du service avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/setDoctorIndispo/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsSetDoctorIndispo(id):
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(id, doc[1], doc[2], doc[3], doc[4], True, doc[6], doc[7])
    flash(f"{doc[2]} {doc[1]} mis en indisponibilité avec succès !", 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/setAgentIndispo/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdSetAgentIndispo(id):
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAge(id, agent[1], agent[2], agent[3], True, agent[5], agent[6], agent[7])
    flash(f"{agent[2]} {agent[1]} mis en indisponibilité avec succès !", 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/unsetDoctorIndispo/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsUnsetDoctorIndispo(id):
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(id, doc[1], doc[2], doc[3], doc[4], False, doc[6], doc[7])
    flash(f"{doc[2]} {doc[1]} retiré de l\'indisponibilité avec succès !", 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/unsetAgentIndispo/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdUnsetAgentIndispo(id):
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAge(id, agent[1], agent[2], agent[3], False, agent[5], agent[6], agent[7])
    flash(f"{agent[2]} {agent[1]} retiré de l\'indisponibilité avec succès !", 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/setDoctor/<int:idDoc>/toSalle/<string:idSalle>', methods=['GET', 'POST'])
@login_required
def lsmsSetDoctorToSalle(idDoc, idSalle):
    LSMSSqlService(f"{current_user.id}-lsms.db").insertSalleDoc(idSalle, idDoc)
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(idDoc)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], doc[6], True)
    flash(f'{doc[2]} {doc[1]} ajouté à la salle avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/setAgent/<int:idAgent>/toSalle/<string:idSalle>', methods=['GET', 'POST'])
@login_required
def lspdSetAgentToSalle(idAgent, idSalle):
    LSPDSqlService(f"{current_user.id}-lspd.db").insertSalleAge(idSalle, idAgent)
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(idAgent)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAge(idAgent, agent[1], agent[2], agent[3], True, agent[5], agent[6], True)
    flash(f'{agent[2]} {agent[1]} ajouté à la salle avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/unsetDoctor/<int:idDoc>/fromSalle/<string:idSalle>', methods=['GET', 'POST'])
@login_required
def lsmsUnsetDoctorFromSalle(idDoc, idSalle):
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteSalleDoc(idDoc, idSalle)
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(idDoc)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], doc[6], False)
    flash(f'{doc[2]} {doc[1]} retiré de la salle avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/unsetAgent/<int:idAgent>/fromSalle/<string:idSalle>', methods=['GET', 'POST'])
@login_required
def lspdUnsetAgentFromSalle(idAgent, idSalle):
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteSalleAge(idAgent, idSalle)
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(idAgent)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAge(idAgent, agent[1], agent[2], agent[3], False, agent[5], agent[6], False)
    flash(f'{agent[2]} {agent[1]} retiré de la salle avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/setDoctor/<int:idDoc>/toIntervention/<int:idInt>', methods=['GET', 'POST'])
@login_required
def lsmsSetDoctorToIntervention(idDoc, idInt):
    LSMSSqlService(f"{current_user.id}-lsms.db").insertIntDoc(idInt, idDoc)
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(idDoc)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], True, doc[7])
    inter = LSMSSqlService(f"{current_user.id}-lsms.db").selectIntById(idInt)
    flash(f'{doc[2]} {doc[1]} ajouté à l\'intervention {inter[1]} avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/setAgent/<int:idAgent>/toIntervention/<int:idInt>', methods=['GET', 'POST'])
@login_required
def lspdSetAgentToIntervention(idAgent, idInt):
    LSPDSqlService(f"{current_user.id}-lspd.db").insertIntAge(idInt, idAgent)
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(idAgent)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAge(idAgent, agent[1], agent[2], agent[3], agent[4], agent[5], True, agent[7])
    inter = LSPDSqlService(f"{current_user.id}-lspd.db").selectIntById(idInt)
    flash(f'{agent[2]} {agent[1]} ajouté à l\'intervention {inter[1]} avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))



# A FIXER CAR SINON CA MARCHE PAS





@app.route('/lsms/unsetDoctor/<int:idDoc>/fromIntervention/<int:idInt>', methods=['GET', 'POST'])
@login_required
def lsmsUnsetDoctorFromIntervention(idDoc, idInt):
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteDocFromInt(idDoc, idInt)
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(idDoc)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], False, doc[7])
    inter = LSMSSqlService(f"{current_user.id}-lsms.db").selectIntById(idInt)
    flash(f'{doc[2]} {doc[1]} retiré de l\'intervention {inter[1]} avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))








@app.route('/lspd/unsetAgent/<int:idAgent>/fromIntervention/<int:idInt>', methods=['GET', 'POST'])
@login_required
def lspdUnsetAgentFromIntervention(idAgent, idInt):
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteAgeFromInt(idAgent, idInt)
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(idAgent)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAge(idAgent, agent[1], agent[2], agent[3], False, agent[5], False, agent[7])
    inter = LSMSSqlService(f"{current_user.id}-lsms.db").selectIntById(idInt)
    flash(f'{agent[2]} {agent[1]} retiré de l\'intervention {inter[1]} avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

if __name__=='__main__':
    args = readArgs()
    port = 9123
    if args.port != None:
        port = args.port
    accounts = AccountService("accounts.db")
    app.run(port=port,host='0.0.0.0', debug=args.debug)
from flask import Flask, render_template, redirect, url_for, flash, request, abort
import flask.cli
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import argparse
from os import urandom
from urllib.parse import urlparse, urljoin
import logging
from datetime import datetime
from hashlib import sha256

from services.flaskForms import AddLsmsForm, EditLsmsForm, AddLspdForm, EditLspdForm ,AddInterventionForm, AddSalleForm, LoginForm, RegisterForm, ModifyAccountForm
from services.regexFunc import RegexUtils
from services.SqlService import LSMSSqlService, LSPDSqlService
from services.ObjectsService import DocteurObj, AgentObj, InterventionObj, SalleObj, AffiliationObj, InterventionDocteursObj, InterventionAgentsObj, AffiliationAgentsObj,InjuredTypeObj
from services.AccountService import AccountService, AccountObject
from services.LoggerService import LoggerService
from services.InjuredService import InjuredService

# ======================================================================================================================
app = Flask(__name__)
secretKey = sha256(datetime.now().strftime("%d%m%Y").encode()).hexdigest()
logger = LoggerService("logs.db", False).insertInfoLog("Server", "Server started with secret key: " + secretKey)
app.config['SECRET_KEY'] = secretKey
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
        LSMSSqlService(f"{userId}-lsms.db").insertDoc(doc.nom, doc.prenom, doc.grade, doc.service, doc.indispo, doc.inInter, doc.inSalle)

def addAgentsToDatabase(userId,agents):
    for agent in agents:
        LSPDSqlService(f"{userId}-lspd.db").insertAgent(agent.matricule, agent.nom, agent.prenom, agent.grade)

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
    parser.add_argument("-ho", "--host", help="Host to run on", type=str)
    args = parser.parse_args()
    return args

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    logger.insertWebLog("Unregistered",f"Unauthorized access to {request.path} from {request.remote_addr}")
    flash('Vous devez être connecté pour accèder à cette page !', 'warning')
    return redirect('/login?next=' + request.path)

@app.errorhandler(400)
def bad_request(e):
    logger.insertErrorLog(current_user.id,f"Bad request from {request.remote_addr} on {request.path} : {e}")
    flash("Requête invalide, si vous estimez que cela n'est pas normal, contactez l'administrateur.", 'danger')
    return render_template('error.html', ErrorCode="400", ErrorMsg="Requête invalide"), 400

@app.errorhandler(404)
def page_not_found(e):
    logger.insertErrorLog(current_user.id,f"Page not found from {request.remote_addr} on {request.path} : {e}")
    flash("Page introuvable, si vous estimez que cela n'est pas normal, contactez l'administrateur.", 'danger')
    return render_template('error.html', ErrorCode="404", ErrorMsg="Page introuvable"), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.insertErrorLog(current_user.id,f"Internal server error from {request.remote_addr} on {request.path} : {e}")
    flash("Erreur interne, si vous estimez que cela n'est pas normal, contactez l'administrateur.", 'danger')
    return render_template('error.html', ErrorCode="500", ErrorMsg="Erreur interne, l'accès a cette page a fini sur une erreur."), 500

@app.errorhandler(502)
def bad_gateway(e):
    logger.insertErrorLog(current_user.id,f"Bad gateway from {request.remote_addr} on {request.path} : {e}")
    flash("Erreur interne, si vous estimez que cela n'est pas normal, contactez l'administrateur.", 'danger')
    return render_template('error.html', ErrorCode="502", ErrorMsg="Erreur interne, l'accès a cette page a fini sur une erreur."), 502

@app.errorhandler(503)
def service_unavailable(e):
    logger.insertErrorLog(current_user.id,f"Service unavailable from {request.remote_addr} on {request.path} : {e}")
    flash("Erreur interne, si vous estimez que cela n'est pas normal, contactez l'administrateur.", 'danger')
    return render_template('error.html', ErrorCode="503", ErrorMsg="Erreur interne, l'accès a cette page a fini sur une erreur."), 503

@app.route('/register', methods=['GET', 'POST'])
def register():
    logger.insertWebLog("Unregistered",f"Access to {request.path} from {request.remote_addr}")
    if current_user.is_authenticated:
        flash("Vous êtes déjà connecté.", 'warning')
        return redirect(url_for('index'))
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
    flash("Le site fermera après le 12/09/2023, merci à tout ceux qui ont utilisé le site ! ❤️", 'warning')
    logger.insertWebLog("Unregistered",f"Access to {request.path} from {request.remote_addr}")
    if current_user.is_authenticated:
        flash("Vous êtes déjà connecté.", 'warning')
        return redirect(url_for('index'))
    next = request.args.get('next')
    if not is_safe_url(next):
        return abort(400)
    form = LoginForm()
    if form.validate_on_submit():
        if accounts.checkAccount(form.usernameLogin.data, form.passwordLogin.data):
            user = User(form.usernameLogin.data)
            user.id = form.usernameLogin.data
            login_user(user)
            logger.insertWebLog(current_user.id,f"Login from {request.remote_addr}")
            return redirect(next or url_for('index'))
        else:
            flash("Mauvais nom d'utilisateur ou mot de passe.", 'danger')
    return render_template('login.html', form=form)

@app.route('/modifyAccount', methods=['GET', 'POST'])
@login_required
def modifyAccount():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    form = ModifyAccountForm()
    if form.validate_on_submit():
        if form.passwordModify.data != form.confirmPasswordModify.data:
            flash('Les mots de passe sont différents.', 'danger')
        else:
            accountId = accounts.getIdByUsername(current_user.id)
            accounts.updateAccount(accountId, current_user.id, form.passwordModify.data)
            flash('Mot de passe modifié !', 'success')
            logger.insertWebLog(current_user.id,f"Password changed from {request.remote_addr}")
            return redirect(url_for('index'))
    return render_template('modifyAccount.html', form=form)

@app.route('/forgotPassword')
def forgotPassword():
    logger.insertWebLog("Unregistered",f"Access to {request.path} from {request.remote_addr}")
    flash("Indisponible sans manipulation administrateur, contactez Wiibleyde", 'warning')
    return redirect(url_for('index'))

@app.route('/deleteAccount')
@login_required
def deleteAccount():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    flash("Indisponible sans manipulation administrateur, contactez Wiibleyde", 'warning')
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    logout_user()
    flash('Vous êtes déconnecté.', 'success')
    logger.insertWebLog("Logout user",f"Logout from {request.remote_addr}")
    return redirect(url_for('login'))

@app.route('/')
@app.route('/index')
@app.route('/home')
@login_required
def index():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    flash("Le site fermera après le 12/09/2023, merci à tout ceux qui ont utilisé le site ! ❤️", 'warning')
    return render_template('index.html')

@app.route('/secret')
@login_required
def secret():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    flash("Le site fermera après le 12/09/2023, merci à tout ceux qui ont utilisé le site ! ❤️", 'warning')
    return render_template('easterEgg/index.html')

@app.route('/admin')
@login_required
def admin():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    currentAccount = accounts.getIdByUsername(current_user.id)
    if accounts.checkIfAdmin(currentAccount):
        accountsList = accounts.getAllAccounts()
        accountObjects = []
        for account in accountsList:
            account = AccountObject(account[0], account[1], account[2], accounts.checkIfAdmin(account[0]))
            accountObjects.append(account)
        return render_template('admin.html', accounts=accountObjects)
    else:
        flash("Vous n'êtes pas administrateur.", 'danger')
        return redirect(url_for('index'))

@app.route('/admin/delete/<accountId>')
@login_required
def adminDeleteAccount(accountId):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    currentAccount = accounts.getIdByUsername(current_user.id)
    if accounts.checkIfAdmin(currentAccount):
        accounts.deleteAccountById(accountId)
        flash("Compte supprimé.", 'success')
        logger.insertWebLog(current_user.id,f"Account {accountId} deleted from {request.remote_addr}")
        return redirect(url_for('admin'))
    else:
        flash("Vous n'êtes pas administrateur.", 'danger')
        return redirect(url_for('index'))
    
@app.route('/admin/setAdmin/<accountId>')
@login_required
def adminSetAdmin(accountId):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    currentAccount = accounts.getIdByUsername(current_user.id)
    if accounts.checkIfAdmin(currentAccount):
        accounts.setAdmin(accountId)
        flash("Compte promu administrateur.", 'success')
        logger.insertWebLog(current_user.id,f"Account {accountId} promoted from {request.remote_addr}")
        return redirect(url_for('admin'))
    else:
        flash("Vous n'êtes pas administrateur.", 'danger')
        return redirect(url_for('index'))
    
@app.route('/admin/unsetAdmin/<accountId>')
@login_required
def adminUnsetAdmin(accountId):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    currentAccount = accounts.getIdByUsername(current_user.id)
    if accounts.checkIfAdmin(currentAccount):
        accounts.unsetAdmin(accountId)
        flash("Compte dégradé.", 'success')
        logger.insertWebLog(current_user.id,f"Account {accountId} degraded from {request.remote_addr}")
        return redirect(url_for('admin'))
    else:
        flash("Vous n'êtes pas administrateur.", 'danger')
        return redirect(url_for('index'))

@app.route('/lscs')
@login_required
def lscs():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    flash("Soon™ (Si quelqu'un demande)", 'warning')
    return redirect(url_for('index'))

@app.route('/bcms')
@login_required
def bcms():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    flash("Soon™ (Si quelqu'un demande)", 'warning')
    return redirect(url_for('index'))

@app.route('/lsms/dispatch', methods=['GET', 'POST'])
@app.route('/lsms', methods=['GET', 'POST'])
@login_required
def lsmsDispatch():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    flash("Le site fermera après le 12/09/2023, merci à tout ceux qui ont utilisé le site ! ❤️", 'warning')
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
    injuredUR = InjuredService(f"{current_user.id}-lsms-injured.json").getUR()
    injuredUA = InjuredService(f"{current_user.id}-lsms-injured.json").getUA()
    injuredDelta = InjuredService(f"{current_user.id}-lsms-injured.json").getDelta()
    injureds = InjuredTypeObj(injuredUR, injuredUA, injuredDelta)
    return render_template('lsms/dispatch.html', form=form, interventions=interventionsObj, salles=sallesObj, doctors=doctorsObj, intDocs=intDocsObj, salleDocs=salleDocsObj, enService=enService, horsService=horsService, injureds=injureds)

@app.route('/lspd/dispatch', methods=['GET', 'POST'])
@app.route('/lspd', methods=['GET', 'POST'])
@login_required
def lspdDispatch():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    flash("Le site fermera après le 12/09/2023, merci à tout ceux qui ont utilisé le site ! ❤️", 'warning')
    form = AddInterventionForm()
    if form.validate_on_submit():
        nom = form.nomInt.data
        exterieur = form.exterieurInt.data
        LSPDSqlService(f"{current_user.id}-lspd.db").insertInt(nom, exterieur)
        flash(f'Intervention {nom} ajoutée avec succès !', 'success')
        return redirect(url_for('lspdDispatch'))
    agents = LSPDSqlService(f"{current_user.id}-lspd.db").selectAllAgents()
    agentsObj = []
    enService = []
    horsService = []
    for agent in agents:
        inInter = False
        inAffiliation = False
        if agent[7] == 1:
            inInter = True
        if agent[8] == 1:
            inAffiliation = True
        agent = AgentObj(agent[0], agent[1], agent[2], agent[3], agent[4], agent[5], agent[6], inInter, inAffiliation)
        agentsObj.append(agent)
    sortAgentsByGrade(agentsObj)
    for agent in agentsObj:
        if agent.service:
            enService.append(agent)
        else:
            horsService.append(agent)
    interventions = LSPDSqlService(f"{current_user.id}-lspd.db").selectAllInterventions()
    interventionsObj = []
    for int in interventions:
        int = InterventionObj(int[0], int[1], int[2])
        interventionsObj.append(int)
    affiliations = LSPDSqlService(f"{current_user.id}-lspd.db").selectAllAffiliations()
    affiliationsObj = []
    for affiliation in affiliations:
        affiliation = AffiliationObj(affiliation[0], affiliation[1])
        affiliationsObj.append(affiliation)
    intAgents = LSPDSqlService(f"{current_user.id}-lspd.db").selectAllInterventionsAgents()
    intAgentsObj = []
    for intAgent in intAgents:
        intAgent = InterventionAgentsObj(intAgent[0], intAgent[1], intAgent[2])
        intAgentsObj.append(intAgent)
    affiliationAgents = LSPDSqlService(f"{current_user.id}-lspd.db").selectAllAffiliationsAgents()
    affiliationAgentsObj = []
    for affiliationAgent in affiliationAgents:
        affiliationAgent = AffiliationAgentsObj(affiliationAgent[0], affiliationAgent[1], affiliationAgent[2])
        affiliationAgentsObj.append(affiliationAgent)
    return render_template('lspd/dispatch.html', form=form, interventions=interventionsObj, affiliations=affiliationsObj, agents=agentsObj, intAgents=intAgentsObj, affiliationAgents=affiliationAgentsObj, enService=enService, horsService=horsService)

@app.route('/lsms/doctors', methods=['GET', 'POST'])
@login_required
def lsmsDoctors():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
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

@app.route('/lsms/doctor/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def lsmsDoctor(doctor_id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    form = EditLsmsForm()
    doctor = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(doctor_id)
    doctor = DocteurObj(*doctor)
    if form.validate_on_submit():
        LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(doctor_id, doctor.nom, doctor.prenom, form.grade.data, doctor.service, doctor.indispo, doctor.inInter, doctor.inSalle)
        flash(f'{doctor.prenom} {doctor.nom} modifié avec succès !', 'success')
        return redirect(url_for('lsmsDoctors'))
    doctor = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(doctor_id)
    doctorObj = DocteurObj(*doctor)
    return render_template('lsms/doctor.html', form=form, doctor=doctorObj)

@app.route('/lspd/agents', methods=['GET', 'POST'])
@login_required
def lspdAgents():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    form = AddLspdForm()
    if form.validate_on_submit():
        if form.matricule.data == '':
            agent = RegexUtils.agentToList(form.zoneText.data, form.grade.data)
            if len(agent) == 0:
                flash(f"Veuillez entrer une ligne d'effectif valide : `    - 00 : Nom Prenom (555-0000)`", 'danger')
                return redirect(url_for('lspdAgents'))
            addAgentsToDatabase(current_user.id, agent)
            strAgent = ''
            for a in agent:
                strAgent += f'{a.matricule} - {a.nom}, '
            flash(f'{strAgent} ajoutés avec succès !', 'success')
            return redirect(url_for('lspdAgents'))
        else:
            agent = RegexUtils.agentToString(form.zoneText.data, form.matricule.data, form.grade.data)
            if agent == None:
                flash(f'Veuillez entrer agent valide ([Prénom] [Nom]) !', 'danger')
                return redirect(url_for('lspdAgents'))
            else:
                LSPDSqlService(f"{current_user.id}-lspd.db").insertAgent(agent.matricule, agent.nom, agent.prenom, agent.grade)
                flash(f'{agent.matricule} - {agent.nom} ajouté avec succès !', 'success')
                return redirect(url_for('lspdAgents'))
    agents = LSPDSqlService(f"{current_user.id}-lspd.db").selectAllAgents()
    agentsObj = []
    for agent in agents:
        agent = AgentObj(*agent)
        agentsObj.append(agent)
    sortAgentsByGrade(agentsObj)
    return render_template('lspd/agents.html', form=form, agents=agentsObj)

@app.route('/lspd/agent/<int:agent_id>', methods=['GET', 'POST'])
@login_required
def lspdAgent(agent_id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    form = EditLspdForm()
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(agent_id)
    agent = AgentObj(*agent)
    if form.validate_on_submit():
        LSPDSqlService(f"{current_user.id}-lspd.db").updateAgent(agent.idAge, agent.matricule, agent.nom, agent.prenom, form.grade.data, agent.service, agent.indispo, agent.inInter, agent.inAffiliation)
        flash(f'{agent.prenom} {agent.nom} modifié avec succès !', 'success')
        return redirect(url_for('lspdAgents'))
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(agent_id)
    agentObj = AgentObj(*agent)
    return render_template('lspd/agent.html', form=form, agent=agentObj)

@app.route('/lsms/salles', methods=['GET', 'POST'])
@login_required
def lsmsSalles():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
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

@app.route('/lspd/addAffiliation', methods=['GET','POST'])
@login_required
def lspdAddAffiliation():
    affiliationType = request.args.get('affiliationType')
    LSPDSqlService(f"{current_user.id}-lspd.db").insertAff(affiliationType)
    flash(f'Affiliation {affiliationType} ajoutée avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/doctor/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsDeleteDoctor(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteDoc(id)
    flash(f'{doc[2]} {doc[1]} supprimé avec succès !', 'success')
    return redirect(url_for('lsmsDoctors'))

@app.route('/lspd/agent/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdDeleteAgent(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteAgent(id)
    flash(f'{agent[2]} {agent[1]} supprimé avec succès !', 'success')
    return redirect(url_for('lspdAgents'))

@app.route('/lsms/salle/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsDeleteSalle(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    salle = LSMSSqlService(f"{current_user.id}-lsms.db").selectSalleById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteSalle(id)
    flash(f'{salle[1]} supprimée avec succès !', 'success')
    return redirect(url_for('lsmsSalles'))

@app.route('/lspd/deleteAffiliation/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdDeleteAffiliation(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    affiliation = LSPDSqlService(f"{current_user.id}-lspd.db").selectAffById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteAff(id)
    agesId = LSPDSqlService(f"{current_user.id}-lspd.db").selectAffAgentByIdAff(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteAffAgentByIdAff(id)
    if agesId:
        for idAge in agesId:
            age = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(idAge[2])
            LSPDSqlService(f"{current_user.id}-lspd.db").updateAgent(age[0], age[1], age[2], age[3], age[4], age[5], age[6], age[7], False)
    flash(f'{affiliation[1]} supprimée avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/deleteIntervention/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsDeleteIntervention(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    inter = LSMSSqlService(f"{current_user.id}-lsms.db").selectIntById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteInt(id)
    docsId = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocByIntId(id)
    if docsId:
        for idDoc in docsId:
            doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(idDoc[2])
            LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(doc[0], doc[1], doc[2], doc[3], doc[4], doc[5], False, doc[7])
    flash(f'{inter[1]} supprimée avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/deleteIntervention/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdDeleteIntervention(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    inter = LSPDSqlService(f"{current_user.id}-lspd.db").selectIntById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteInt(id)
    agesId = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgentByIdInt(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteIntAgentByIdInt(id)
    if agesId:
        for idAge in agesId:
            age = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(idAge[2])
            LSPDSqlService(f"{current_user.id}-lspd.db").updateAgent(age[0], age[1], age[2], age[3], age[4], age[5], age[6], False, age[8])
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/setDoctorService/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsSetDoctorServer(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(id, doc[1], doc[2], doc[3], True, doc[5], doc[6], doc[7])
    flash(f'{doc[2]} {doc[1]} ajouté au service avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/setAgentService/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdSetAgentServer(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAgent(id, agent[1], agent[2], agent[3], agent[4], True, agent[6], agent[7], agent[8])
    flash(f'{agent[2]} {agent[1]} ajouté au service avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/unsetDoctorService/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsUnsetDoctorServer(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(id, doc[1], doc[2], doc[3], False, False, False, False)
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteIntDocByDocId(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteSalleDocByDocId(id)
    flash(f'{doc[2]} {doc[1]} retiré du service avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lsms/unsetAllDoctorsService', methods=['GET', 'POST'])
@login_required
def lsmsUnsetAllDoctorsServer():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    doctors = LSMSSqlService(f"{current_user.id}-lsms.db").selectDoc()
    for doc in doctors:
        LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(doc[0], doc[1], doc[2], doc[3], False, False, False, False)
        LSMSSqlService(f"{current_user.id}-lsms.db").deleteIntDocByDocId(doc[0])
        LSMSSqlService(f"{current_user.id}-lsms.db").deleteSalleDocByDocId(doc[0])
    flash(f'Tous les docteurs retirés du service avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/unsetAgentService/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdUnsetAgentServer(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAgent(id, agent[1], agent[2], agent[3], agent[4], False, False, False, False)
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteIntAgentByIdAgent(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteAffAgentByIdAgent(id)
    flash(f'{agent[2]} {agent[1]} retiré du service avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lspd/unsetAllAgentsService', methods=['GET', 'POST'])
@login_required
def lspdUnsetAllAgentsServer():
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    agents = LSPDSqlService(f"{current_user.id}-lspd.db").selectAllAgents()
    for agent in agents:
        LSPDSqlService(f"{current_user.id}-lspd.db").updateAgent(agent[0], agent[1], agent[2], agent[3], agent[4], False, False, False, False)
        LSPDSqlService(f"{current_user.id}-lspd.db").deleteIntAgentByIdAgent(agent[0])
        LSPDSqlService(f"{current_user.id}-lspd.db").deleteAffAgentByIdAgent(agent[0])
    flash(f'Tous les agents retirés du service avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/setDoctorIndispo/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsSetDoctorIndispo(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(id, doc[1], doc[2], doc[3], doc[4], True, doc[6], doc[7])
    flash(f"{doc[2]} {doc[1]} mis en indisponibilité avec succès !", 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/setAgentIndispo/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdSetAgentIndispo(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAgent(id, agent[1], agent[2], agent[3], agent[4], agent[5], True, agent[7], agent[8])
    flash(f"{agent[2]} {agent[1]} mis en indisponibilité avec succès !", 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/unsetDoctorIndispo/<int:id>', methods=['GET', 'POST'])
@login_required
def lsmsUnsetDoctorIndispo(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(id)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(id, doc[1], doc[2], doc[3], doc[4], False, doc[6], doc[7])
    flash(f"{doc[2]} {doc[1]} retiré de l\'indisponibilité avec succès !", 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/unsetAgentIndispo/<int:id>', methods=['GET', 'POST'])
@login_required
def lspdUnsetAgentIndispo(id):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(id)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAgent(id, agent[1], agent[2], agent[3], agent[4], agent[5], False, agent[7], agent[8])
    flash(f"{agent[2]} {agent[1]} retiré de l\'indisponibilité avec succès !", 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/setDoctor/<int:idDoc>/toSalle/<int:idSalle>', methods=['GET', 'POST'])
@login_required
def lsmsSetDoctorToSalle(idDoc, idSalle):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    LSMSSqlService(f"{current_user.id}-lsms.db").insertSalleDoc(idSalle, idDoc)
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(idDoc)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], doc[6], True)
    flash(f'{doc[2]} {doc[1]} ajouté à la salle avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/setAgent/<int:idDoc>/toAffiliation/<int:idAff>', methods=['GET', 'POST'])
@login_required
def lspdSetAgentToAffiliation(idDoc, idAff):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    LSPDSqlService(f"{current_user.id}-lspd.db").insertAffAgent(idAff, idDoc)
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(idDoc)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAgent(idDoc, agent[1], agent[2], agent[3], agent[4], agent[5], agent[6], agent[7], True)
    aff = LSPDSqlService(f"{current_user.id}-lspd.db").selectAffById(idAff)
    flash(f'{agent[2]} {agent[1]} ajouté à l\'affiliation {aff[1]} avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/unsetDoctor/<int:idDoc>/fromSalle/<int:idSalle>', methods=['GET', 'POST'])
@login_required
def lsmsUnsetDoctorFromSalle(idDoc, idSalle):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteSalleDoc(idDoc, idSalle)
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(idDoc)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], doc[6], False)
    flash(f'{doc[2]} {doc[1]} retiré de la salle avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/unsetAgent/<int:idAgent>/fromAffiliation/<int:idAff>', methods=['GET', 'POST'])
@login_required
def lspdUnsetAgentFromAffiliation(idAgent, idAff):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteAgentFromAff(idAgent, idAff)
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(idAgent)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAgent(idAgent, agent[1], agent[2], agent[3], agent[4], agent[5], agent[6], agent[7], False)
    aff = LSPDSqlService(f"{current_user.id}-lspd.db").selectAffById(idAff)
    flash(f'{agent[2]} {agent[1]} retiré de l\'affiliation {aff[1]} avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/setDoctor/<int:idDoc>/toIntervention/<int:idInt>', methods=['GET', 'POST'])
@login_required
def lsmsSetDoctorToIntervention(idDoc, idInt):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    LSMSSqlService(f"{current_user.id}-lsms.db").insertIntDoc(idInt, idDoc)
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(idDoc)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], True, doc[7])
    inter = LSMSSqlService(f"{current_user.id}-lsms.db").selectIntById(idInt)
    flash(f'{doc[2]} {doc[1]} ajouté à l\'intervention {inter[1]} avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/setAgent/<int:idAgent>/toIntervention/<int:idInt>', methods=['GET', 'POST'])
@login_required
def lspdSetAgentToIntervention(idAgent, idInt):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    LSPDSqlService(f"{current_user.id}-lspd.db").insertIntAgent(idInt, idAgent)
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(idAgent)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAgent(idAgent, agent[1], agent[2], agent[3], agent[4], agent[5], agent[6], True, agent[8])
    inter = LSPDSqlService(f"{current_user.id}-lspd.db").selectIntById(idInt)
    flash(f'{agent[2]} {agent[1]} ajouté à l\'intervention {inter[1]} avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/unsetDoctor/<int:idDoc>/fromIntervention/<int:idInt>', methods=['GET', 'POST'])
@login_required
def lsmsUnsetDoctorFromIntervention(idDoc, idInt):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    LSMSSqlService(f"{current_user.id}-lsms.db").deleteDocFromInt(idDoc, idInt)
    doc = LSMSSqlService(f"{current_user.id}-lsms.db").selectDocById(idDoc)
    LSMSSqlService(f"{current_user.id}-lsms.db").updateDoc(idDoc, doc[1], doc[2], doc[3], doc[4], doc[5], False, doc[7])
    inter = LSMSSqlService(f"{current_user.id}-lsms.db").selectIntById(idInt)
    flash(f'{doc[2]} {doc[1]} retiré de l\'intervention {inter[1]} avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lspd/unsetAgent/<int:idAgent>/fromIntervention/<int:idInt>', methods=['GET', 'POST'])
@login_required
def lspdUnsetAgentFromIntervention(idAgent, idInt):
    logger.insertWebLog(current_user.id,f"Access to {request.path} from {request.remote_addr}")
    LSPDSqlService(f"{current_user.id}-lspd.db").deleteAgentFromInt(idAgent, idInt)
    agent = LSPDSqlService(f"{current_user.id}-lspd.db").selectAgeById(idAgent)
    LSPDSqlService(f"{current_user.id}-lspd.db").updateAgent(idAgent, agent[1], agent[2], agent[3], agent[4], agent[5], agent[6], False, agent[8])
    inter = LSPDSqlService(f"{current_user.id}-lspd.db").selectIntById(idInt)
    flash(f'{agent[2]} {agent[1]} retiré de l\'intervention {inter[1]} avec succès !', 'success')
    return redirect(url_for('lspdDispatch'))

@app.route('/lsms/addInjured', methods=['GET', 'POST'])
@login_required
def lsmsAddInjured():
    injuredType = request.args.get('injuredType')
    if injuredType == "UR":
        InjuredService(f"{current_user.id}-lsms-injured.json").addUR()
    elif injuredType == "UA":
        InjuredService(f"{current_user.id}-lsms-injured.json").addUA()
    elif injuredType == "DELTA":
        InjuredService(f"{current_user.id}-lsms-injured.json").addDelta()
    else:
        flash(f'Erreur lors de l\'ajout du blessé !', 'danger')
        return redirect(url_for('lsmsDispatch'))
    flash(f'Blessé ajouté avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lsms/removeInjured', methods=['GET', 'POST'])
@login_required
def lsmsRemoveInjured():
    injuredType = request.args.get('injuredType')
    if injuredType == "UR":
        if not InjuredService(f"{current_user.id}-lsms-injured.json").removeUR():
            flash(f'Erreur lors de la suppression du blessé !', 'danger')
            return redirect(url_for('lsmsDispatch'))
    elif injuredType == "UA":
        if not InjuredService(f"{current_user.id}-lsms-injured.json").removeUA():
            flash(f'Erreur lors de la suppression du blessé !', 'danger')
            return redirect(url_for('lsmsDispatch'))
    elif injuredType == "DELTA":
        if not InjuredService(f"{current_user.id}-lsms-injured.json").removeDelta():
            flash(f'Erreur lors de la suppression du blessé !', 'danger')
            return redirect(url_for('lsmsDispatch'))
    else:
        flash(f'Erreur lors de la suppression du blessé !', 'danger')
        return redirect(url_for('lsmsDispatch'))
    flash(f'Blessé supprimé avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

@app.route('/lsms/resetInjured', methods=['GET', 'POST'])
@login_required
def lsmsResetInjured():
    InjuredService(f"{current_user.id}-lsms-injured.json").reset()
    flash(f'Blessés réinitialisés avec succès !', 'success')
    return redirect(url_for('lsmsDispatch'))

if __name__=='__main__':
    args = readArgs()
    logger = LoggerService("logs.db", args.debug)
    logger.insertInfoLog("Server", "Starting server")
    port = 9123
    host = '0.0.0.0'
    if args.port != None:
        port = args.port
    if args.host != None:
        host = args.host
    accounts = AccountService("accounts.db")
    flaskLog = logging.getLogger('werkzeug')
    flaskLog.disabled = True
    flask.cli.show_server_banner = lambda *args: None
    logger.insertInfoLog("Web Server", f"Starting web server on {host}:{port}")
    app.run(port=port,host=host,debug=args.debug)
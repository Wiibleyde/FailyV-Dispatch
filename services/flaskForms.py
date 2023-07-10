from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField, PasswordField
from wtforms.validators import DataRequired

class AddLspdForm(FlaskForm):
    zoneText = TextAreaField('zoneText', validators=[DataRequired()], render_kw={"placeholder": "Ligne d'effectif","autofocus": True})
    grade = SelectField('grade', choices=[('Commissaire', 'Commissaire'), ('Capitaine', 'Capitaine'), ('Lieutenant', 'Lieutenant'), ('Inspecteur', 'Inspecteur'), ('Sergent Chef', 'Sergent Chef'), ('Sergent', 'Sergent'), ('Officier Supérieur','Officier Supérieur'), ('Officier','Officier'),('Cadet','Cadet')])
    matricule = StringField('matricule', render_kw={"placeholder": "Matricule (vide si plusieurs agents)","autofocus": True})
    submitDoc = SubmitField('submitDoc', render_kw={"value": "Ajouter l'agent"})

class EditLspdForm(FlaskForm):
    grade = SelectField('grade', choices=[('Commissaire', 'Commissaire'), ('Capitaine', 'Capitaine'), ('Lieutenant', 'Lieutenant'), ('Inspecteur', 'Inspecteur'), ('Sergent Chef', 'Sergent Chef'), ('Sergent', 'Sergent'), ('Officier Supérieur','Officier Supérieur'), ('Officier','Officier'),('Cadet','Cadet')])
    submitDoc = SubmitField('submitDoc', render_kw={"value": "Modifier le grade"})

class AddLsmsForm(FlaskForm):
    zoneText = TextAreaField('zoneText', validators=[DataRequired()], render_kw={"placeholder": "Ligne d'effectif","autofocus": True})
    grade = SelectField('grade', choices=[('Directeur', 'Directeur'), ('Directeur Adjoint', 'Directeur Adjoint'), ('Chef de service', 'Chef de service'), ('Spécialiste', 'Spécialiste'), ('Titulaire', 'Titulaire'), ('Résident', 'Résident'), ('Interne', 'Interne')])
    submitDoc = SubmitField('submitDoc', render_kw={"value": "Ajouter le docteur"})

class EditLsmsForm(FlaskForm):
    grade = SelectField('grade', choices=[('Directeur', 'Directeur'), ('Directeur Adjoint', 'Directeur Adjoint'), ('Chef de service', 'Chef de service'), ('Spécialiste', 'Spécialiste'), ('Titulaire', 'Titulaire'), ('Résident', 'Résident'), ('Interne', 'Interne')])
    submitDoc = SubmitField('submitDoc', render_kw={"value": "Modifier le grade"})

class AddInterventionForm(FlaskForm):
    nomInt = StringField('nomInt', validators=[DataRequired()], render_kw={"placeholder": "Nom de l'intervention","autofocus": True})
    exterieurInt = BooleanField('exterieurInt')
    submitInt = SubmitField('submitInt', render_kw={"value": "Créer l'intervention"})

class AddSalleForm(FlaskForm):
    nomSalle = StringField('nomSalle', validators=[DataRequired()], render_kw={"placeholder": "Nom de la salle","autofocus": True})
    submitSalle = SubmitField('submitSalle', render_kw={"value": "Créer la salle"})

class LoginForm(FlaskForm):
    usernameLogin = StringField('usernameLogin', validators=[DataRequired()], render_kw={"placeholder": "Nom d'utilisateur","autofocus": True, "class": "text-black"})
    passwordLogin = PasswordField('passwordLogin', validators=[DataRequired()], render_kw={"placeholder": "Mot de passe", "class": "text-black"})
    submitLogin = SubmitField('submitLogin', render_kw={"value": "Se connecter"})

class RegisterForm(FlaskForm):
    usernameRegister = StringField('usernameRegister', validators=[DataRequired()], render_kw={"placeholder": "Nom d'utilisateur","autofocus": True})
    passwordRegister = PasswordField('passwordRegister', validators=[DataRequired()], render_kw={"placeholder": "Mot de passe"})
    confirmPasswordRegister = PasswordField('confirmPasswordRegister', validators=[DataRequired()], render_kw={"placeholder": "Confirmer le mot de passe"})
    submitRegister = SubmitField('submitRegister', render_kw={"value": "S'inscrire"})

class ModifyAccountForm(FlaskForm):
    passwordModify = PasswordField('passwordModify', validators=[DataRequired()], render_kw={"placeholder": "Mot de passe"})
    confirmPasswordModify = PasswordField('confirmPasswordModify', validators=[DataRequired()], render_kw={"placeholder": "Confirmer le mot de passe"})
    submitModify = SubmitField('submitModify', render_kw={"value": "Modifier le compte"})
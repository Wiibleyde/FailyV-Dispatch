from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class AddDocteurForm(FlaskForm):
    zoneText = TextAreaField('zoneText', validators=[DataRequired()], render_kw={"placeholder": "Ligne d'effectif","autofocus": True})
    grade = SelectField('grade', choices=[('Directeur', 'Directeur'), ('Directeur Adjoint', 'Directeur Adjoint'), ('Chef de service', 'Chef de service'), ('Spécialiste', 'Spécialiste'), ('Titulaire', 'Titulaire'), ('Résident', 'Résident'), ('Interne', 'Interne')])
    submitDoc = SubmitField('submitDoc', render_kw={"value": "Ajouter le docteur"})

class AddInterventionForm(FlaskForm):
    nomInt = StringField('nomInt', validators=[DataRequired()], render_kw={"placeholder": "Nom de l'intervention","autofocus": True})
    exterieurInt = BooleanField('exterieurInt')
    submitInt = SubmitField('submitInt', render_kw={"value": "Créer l'intervention"})

class AddSalleForm(FlaskForm):
    nomSalle = StringField('nomSalle', validators=[DataRequired()], render_kw={"placeholder": "Nom de la salle","autofocus": True})
    submitSalle = SubmitField('submitSalle', render_kw={"value": "Créer la salle"})
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class AddDocteurForm(FlaskForm):
    zoneText = TextAreaField('zoneText', validators=[DataRequired()], render_kw={"placeholder": "Ligne d'effectif"})
    grade = SelectField('grade', choices=[('Directeur', 'Directeur'), ('Directeur Adjoint', 'Directeur Adjoint'), ('Chef de service', 'Chef de service'), ('Spécialiste', 'Spécialiste'), ('Titulaire', 'Titulaire'), ('Résident', 'Résident'), ('Interne', 'Interne')])
    submitDoc = SubmitField('submitDoc', render_kw={"value": "Ajouter le docteur"})

class AddInterventionForm(FlaskForm):
    nomInt = StringField('nomInt', validators=[DataRequired()], render_kw={"placeholder": "Nom de l'intervention"})
    exterieurInt = BooleanField('exterieurInt')
    submitInt = SubmitField('submitInt', render_kw={"value": "Créer l'intervention"})

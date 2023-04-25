from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, BooleanField
from wtforms.validators import DataRequired

class AddDocteurForm(FlaskForm):
    nomDoc = StringField('Nom', [validators.Length(min=1, max=50)])
    prenomDoc = StringField('Prenom', [validators.Length(min=1, max=50)])
    gradeDoc = StringField('Grade', [validators.Length(min=1, max=50)])
    submitDoc = SubmitField('Submit', [validators.Length(min=1, max=50)])

class AddInterventionForm(FlaskForm):
    nomInt = StringField('nomInt', validators=[DataRequired()], render_kw={"placeholder": "Nom de l'intervention"})
    exterieurInt = BooleanField('exterieurInt')
    submitInt = SubmitField('submitInt', render_kw={"value": "Créer l'intervention"})

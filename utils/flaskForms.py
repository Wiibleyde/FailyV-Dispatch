from flask_wtf import Form
from wtforms import StringField, validators, SubmitField, BooleanField

class AddDocteurForm(Form):
    nomDoc = StringField('Nom', [validators.Length(min=1, max=50)])
    prenomDoc = StringField('Prenom', [validators.Length(min=1, max=50)])
    gradeDoc = StringField('Grade', [validators.Length(min=1, max=50)])
    submitDoc = SubmitField('Submit', [validators.Length(min=1, max=50)])

class AddInterventionForm(Form):
    nomInt = StringField('Nom', [validators.Length(min=1, max=50)])
    exterieurInt = BooleanField('Exterieur')
    submitInt = SubmitField('Submit', [validators.Length(min=1, max=50)])

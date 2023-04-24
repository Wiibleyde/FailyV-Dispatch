from wtforms import Form, StringField, validators

class AddDocteurForm(Form):
    nomDoc = StringField('Nom', [validators.Length(min=1, max=50)])
    prenomDoc = StringField('Prenom', [validators.Length(min=1, max=50)])
    gradeDoc = StringField('Grade', [validators.Length(min=1, max=50)])
    submitDoc = StringField('Submit', [validators.Length(min=1, max=50)])

class AddInterventionForm(Form):
    nomInt = StringField('Nom', [validators.Length(min=1, max=50)])
    exterieurInt = StringField('Exterieur', [validators.Length(min=1, max=50)])
    submitInt = StringField('Submit', [validators.Length(min=1, max=50)])

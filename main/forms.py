from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields import TextField, HiddenField, FloatField, SelectField

class NodeForm(Form):
    id = HiddenField('Id')
    new = HiddenField('New')
    name = TextField('Name',[validators.Required()])
    leader  = SelectField('Leader', choices=[], coerce=int)
    lat = FloatField('Latitude', [validators.Required()])
    lon = FloatField('Longitude', [validators.Required()])
    
    def validate(self):
        valid = True
        rv = Form.validate(self)
        if not rv:
            valid = False
        return valid
from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields import TextField, HiddenField, FloatField, SelectField, FieldList, FormField
import wtforms

class LocationForm(wtforms.Form):
    lat = FloatField('Latitude', [validators.Required()])
    lon = FloatField('Longitude', [validators.Required()])

class JumpPointForm(wtforms.Form):
    id = HiddenField('Id')
    pos = HiddenField('Position')
    lat = FloatField('Latitude', [validators.Required()])
    lon = FloatField('Longitude', [validators.Required()])
    
class NodeForm(Form):
    id = HiddenField('Id')
    new = HiddenField('New')
    name = TextField('Name',[validators.Required()])
    leader  = SelectField('Leader', choices=[], coerce=int)
    location = FormField(LocationForm)
    jumppoints = FieldList(FormField(JumpPointForm))
    
    def validate(self):
        valid = True
        rv = Form.validate(self)
        if not rv:
            valid = False
        return valid
    
class ObstacleForm(Form):
    id = HiddenField('Id')
    new = HiddenField('New')
    location = FormField(LocationForm)
    
    def validate(self):
        valid = True
        rv = Form.validate(self)
        if not rv:
            valid = False
        return valid
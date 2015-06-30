from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields import TextField, HiddenField, FloatField, SelectField, FieldList, FormField
import wtforms

class LocationForm(wtforms.Form):
    lat = FloatField('Latitude', [validators.Required()])
    lon = FloatField('Longitude', [validators.Required()])

class PathPointForm(wtforms.Form):
    pid = HiddenField('Id')
    lat = FloatField('Latitude', [validators.Required()])
    lon = FloatField('Longitude', [validators.Required()])
    
class NodeForm(Form):
    id = HiddenField('Id')
    new = HiddenField('New')
    name = TextField('Name',[validators.Required()])
    leader  = SelectField('Leader', choices=[], coerce=int)
    location = FormField(LocationForm)
    
    def validate(self):
        valid = True
        rv = Form.validate(self)
        if not rv:
            valid = False
        return valid
    
class PointForm(Form):
    id = HiddenField('Id')
    new = HiddenField('New')
    location = FormField(LocationForm)
    
    def validate(self):
        valid = True
        rv = Form.validate(self)
        if not rv:
            valid = False
        return valid
    
class PathForm(Form):
    id = HiddenField('Id')
    new = HiddenField('New')
    node  = SelectField('Node', choices=[], coerce=int)
    points = FieldList(FormField(PathPointForm))
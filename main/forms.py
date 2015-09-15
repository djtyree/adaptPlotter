from flask.ext.wtf import Form
from wtforms import validators
from wtforms.fields import TextField, HiddenField, FloatField, SelectField, FieldList, FormField
import wtforms
from wtforms.fields.core import IntegerField

class LocationForm(wtforms.Form):
    lat = FloatField('Latitude', [validators.Required()])
    lon = FloatField('Longitude', [validators.Required()])

class JumpPointForm(wtforms.Form):
    jp_id = HiddenField('JumpPoint Id')
    pos = HiddenField('Position')
    lat = FloatField('Latitude', [validators.Required()])
    lon = FloatField('Longitude', [validators.Required()])

class GoalForm(wtforms.Form):
    goal_id = HiddenField('Goal Id')
    pos = HiddenField('Position')
    lat = FloatField('Latitude', [validators.Required()])
    lon = FloatField('Longitude', [validators.Required()])
    
class NodeForm(Form):
    id = HiddenField('Id')
    new = HiddenField('New')
    name = TextField('Name',[validators.Required()])
    rid = IntegerField("Robot ID",[validators.Required()])
    leader  = SelectField('Leader', choices=[], coerce=int)
    location = FormField(LocationForm)
    jumppoints = FieldList(FormField(JumpPointForm))
    goals = FieldList(FormField(GoalForm))
    
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
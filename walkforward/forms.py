from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, MultipleFileField, SubmitField, SelectField
from wtforms.fields.html5 import IntegerRangeField

class UploadFileForm(FlaskForm):
    data_files = MultipleFileField('File(s) Upload', validators = [FileAllowed('csv', 'txt')])
    submit = SubmitField('Proceed')

class SidebarForm(FlaskForm):
    wf_type = SelectField('Choose the Walk_forward type', 
                        choices = [('anchored', 'Anchored Walk Forward'), ('unanchored', 'Unanchored Walk Forward')])
    in_range = IntegerRangeField('Select in sample range')
    out_range = IntegerRangeField('Select out sample range')
    submit = SubmitField('Create Graphs')

    
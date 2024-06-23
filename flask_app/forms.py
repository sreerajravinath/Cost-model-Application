from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, Optional

class GenericModelForm(FlaskForm):
    submit = SubmitField('Submit')

    @classmethod
    def create_form(cls, fields_config):
        form_class = type('DynamicModelForm', (cls,), {})
        for field_name, field_config in fields_config.items():
            if field_config['type'] == 'string':
                setattr(form_class, field_name, StringField(field_config['label'], validators=[DataRequired()]))
            elif field_config['type'] == 'integer':
                setattr(form_class, field_name, IntegerField(field_config['label'], validators=[DataRequired()]))
            elif field_config['type'] == 'select':
                choices = [(choice['value'], choice['label']) for choice in field_config['choices']]
                setattr(form_class, field_name, SelectField(field_config['label'], choices=choices, validators=[DataRequired()]))
            elif field_config['type'] == 'radio':
                choices = [(choice['value'], choice['label']) for choice in field_config['choices']]
                setattr(form_class, field_name, RadioField(field_config['label'], choices=choices, validators=[DataRequired()]))
        return form_class

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, ValidationError, NumberRange


city_group = ('Johor', 'Kedah', 'Kelantan', 'Kuala Lumpur', 'Labuan', 'Melaka', 'Negeri Sembilan', 'Pahang', 'Penang',
              'Perak', 'Perlis', 'Putrajaya', 'Sabah', 'Sarawak', 'Selangor', 'Terengganu')


class PurchaseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2)])
    phone = StringField(label='Mobile No', validators=[DataRequired(), Length(min=10, max=11,
                                                            message="Mobile No should consist digits only.")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    add1 = StringField('Address 1', validators=[DataRequired()])
    add2 = StringField('Address 2', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = SelectField(label='State', choices=[(group, group) for group in city_group])
    postcode = StringField(label='Postcode',
                           validators=[DataRequired(), Length(min=5, max=5,
                                                              message="Postcode should be 5 digits only.")])
    submit = SubmitField('Continue')

    def validate_phone(self, phone):
        print("im here a1")
        if len(phone.data) > 11:
            print("im here 1")
            raise ValidationError('Invalid Mobile Number.')
        if not str(phone.data).isdigit():
            print("im here 2")
            raise ValidationError('Mobile Number should consist digit only.')

    def validate_postcode(self, postcode):
        if len(postcode.data) > 5:
            raise ValidationError('Invalid Postcode.')
        if not str(postcode.data).isdigit():
            raise ValidationError('Invalid Postcode.')





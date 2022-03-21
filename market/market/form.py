from cProfile import label
from unicodedata import name
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import DataRequired,length,EqualTo,ValidationError
from market.model import User

class RegisterForm(FlaskForm):
    name = StringField(label='Name' , validators=[DataRequired() , length(max=20)])
    password = PasswordField(label = 'Password' ,validators=[DataRequired() , length(max=40 , min=8)])
    repeatpassword = PasswordField(label = 'Confirm Password',validators=[DataRequired() , length(max=40 , min=8) , EqualTo('password')])
    submit = SubmitField(label = 'Create account')
    def validate_name(self, name_to_check):
        if(User.query.filter_by(name = name_to_check.data).first()):
            raise ValidationError('Username already exist! please try another username')
        
class SignForm(FlaskForm):
    name = StringField(label='Name' , validators=[DataRequired() , length(max=20)])
    password = PasswordField(label = 'Password' ,validators=[DataRequired() , length(max=40 , min=8)])
    submit = SubmitField(label = 'Sign in')


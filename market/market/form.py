from cProfile import label
from unicodedata import category
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , IntegerField
from wtforms.validators import DataRequired,length,EqualTo,ValidationError
from market.model import Item, User

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

class AddItemForm(FlaskForm):
    
    product_name = StringField(label='Product name' , validators=[DataRequired()  , length(max=20)])
    barcode = IntegerField(label='barcode' , validators=[DataRequired() ])
    category = StringField(label='category' , validators=[DataRequired()])
    price = IntegerField(label='price' , validators=[DataRequired()])
    description = StringField(label='description' , validators=[DataRequired()])
    submit = SubmitField(label = 'Add Item')
    
class ModifyItemForm(FlaskForm):
    
    product_name = StringField(label='Product name' , validators=[DataRequired()  , length(max=20)])
    barcode = IntegerField(label='barcode' , validators=[DataRequired() , length(max=20)])
    category = StringField(label='category' , validators=[DataRequired()])
    price = IntegerField(label='price' , validators=[DataRequired()])
    description = StringField(label='description' , validators=[DataRequired()])
    submit = SubmitField(label = 'Modify Item')
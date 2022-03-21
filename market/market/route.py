from crypt import methods
from sre_constants import SUCCESS
from unicodedata import name
from flask import redirect, render_template, url_for,flash
from flask_login import login_user
from market import app,db
from market.form import RegisterForm, SignForm
from market.model import User

@app.route('/')
def home_page():
    return render_template('dashboard.html')


@app.route('/Dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/Signup' , methods = ['GET' , 'POST'])
def signup_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User (name = form.name.data ,hash_password = form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return (redirect(url_for('dashboard_page')))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error while creating a user: {err_msg}', category='danger')
    
    return render_template('signup.html' , form = form)

@app.route('/Signin' , methods = ['GET' , 'POST'])
def signin_page():
    form = SignForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name = form.name.data).first()
        if (user.hash_password == form.name.data.bcrypt()):
            login_user(user)
            flash('Congratulation you re logged in' , category='success')
            return (redirect(url_for(dashboard_page)))
        else:
            flash('Username and password does not match please try again', category='danger')
    
    return render_template('signin.html')
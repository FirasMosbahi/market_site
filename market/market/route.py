from unicodedata import category
from market import app , db
from flask import render_template, redirect, url_for, flash
from market import form
from market.model import Item, User
from market.form import AddItemForm, RegisterForm, SignForm , ModifyItemForm
from flask_login import current_user, login_user , logout_user

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
        user_to_create = User (name = form.name.data ,password = form.password.data)
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
        attempted_user = User.query.filter_by(name = form.name.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):            
            login_user(attempted_user)
            flash('Congratulation you re logged in' , category='success')
            return (redirect(url_for('dashboard_page')))
        else:
            flash('Username and password does not match please try again', category='danger')
    
    return render_template('signin.html' , form = form)

@app.route('/logout')
def logout_page():
    if (not current_user.is_authenticated):
        flash("There is no authenticated user", category='danger')

    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("dashboard_page"))

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html' , items = items)

@app.route('/addItem' , methods = ['GET' , 'POST'])
def add_item_page():
    form = AddItemForm()
    if form.validate_on_submit():
        if (current_user):
            item_to_create = Item (barcode = form.barcode.data , name = form.product_name.data , price = form.price.data , description = form.description.data , owner = current_user.id)
            db.session.add(item_to_create)
            db.session.commit()
            return redirect(url_for('market_page'))
        
        else:
            flash ('An user should be authentificated before creating an item', category='danger')
            return redirect(url_for(signin_page))
        
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error while creating an item: {err_msg}', category='danger')
    
    return render_template('itemadd.html' , form = form , title = 'Item add' , product_name = '' , barcode = '' , price = '' , category = '' , description = '')

@app.route('/modifyItem/<item_id>' , methods = ['GET' , 'POST'])
def modify_item_page(item_id):
    form = ModifyItemForm()
    if form.validate_on_submit():
        if (current_user and current_user.id == Item.query.filter_by(id = item_id).first().owner):
            Item.query.filter_by(id = item_id).first().barcode = form.barcode.data
            Item.query.filter_by(id = item_id).first().name = form.product_name.data
            Item.query.filter_by(id = item_id).first().category = form.category.data
            Item.query.filter_by(id = item_id).first().price = form.price.data
            Item.query.filter_by(id = item_id).first().description = form.description.data
            db.session.commit()
            return redirect(url_for('market_page'))
              
        else:
            flash ('Only item owner is able to modify his own item', category='danger')
            return redirect(url_for(signin_page))
        
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error while modifying item : {err_msg}', category='danger')
    
    return render_template('itemadd.html' , form = form , title = 'item ' + item_id + ' modifying' , product_name = Item.query.filter_by(id = item_id).first().name , barcode = Item.query.filter_by(id = item_id).first().barcode , price = Item.query.filter_by(id = item_id).first().price , category = Item.query.filter_by(id = item_id).first().category , description = Item.query.filter_by(id = item_id).first().description)

@app.route('/buyItem/<item_id>')
def buy_item(item_id):
    if(not current_user):
        flash ('you can not buy item without log in' , category = 'danger')
        return redirect(url_for('signin_page'))
    
    if(Item.query.filter_by(id = item_id).first().owner == current_user.id):
        flash ('you are the owner ofthis item' , category='info')
        return redirect(url_for('market_page'))
    
    if (Item.query.filter_by(id = item_id).first().price > current_user.solde):
        flash ('insufficient solde' , category = 'danger')
        return redirect(url_for('market_page'))

    Item.query.filter_by(id = item_id).first().owner = current_user.id
    User.query.fliter_by(id = current_user.id).first().solde -= Item.query.filter_by(id = item_id).first().price
    db.session.commit()
    flash ('Congratulation : the item was bought successfuly' , category = 'success')
    return redirect(url_for('market_page'))

@app.route('/sellItem/<item_id>')
def delete_item(item_id):
    if (current_user.id != Item.query.filter_by(id = item_id).first().owner):
        flash ('you can not delete an item without being his owner' , category = 'info')
        return redirect(url_for('market_page'))
    
    db.session.remove(Item.query.filter_by(id = item_id).first())
    db.session.commit()
    return redirect(url_for('market_page'))
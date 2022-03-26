from market import db , login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model,UserMixin):
    id = db.Column (db.Integer() , primary_key = True)
    name = db.Column (db.String(length = 20) , nullable = False , unique = True)
    password_hash = db.Column (db.String(length = 255) , nullable = False)
    solde = db.Column (db.Integer() , nullable = False , default = 999)
    items = db.relationship('Item' , backref = 'owned_item' , lazy = True)
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
          
     
class Item(db.Model):
    id = db.Column (db.Integer() , primary_key = True)
    barcode = db.Column (db.Integer() , nullable = False)
    name = db.Column (db.String(length = 20) , nullable = False)
    price = db.Column (db.Integer() , nullable = False)
    description = db.Column (db.String(length = 200) , nullable = False)
    owner = db.Column(db.Integer() , db.ForeignKey(User.id))
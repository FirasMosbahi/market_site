from market import db

class User(db.Model):
    id = db.Column (db.Integer() , primary_key = True)
    name = db.Column (db.String(length = 20) , nullable = False , unique = True)
    hash_password = db.Column (db.String(length = 255) , nullable = False)
    solde = db.Column (db.Integer() , nullable = False , default = 999)
    #items = db.relationship('Item' , backref = 'owned_item' , lazy = True)
    
    
class Item(db.Model):
    id = db.Column (db.Integer() , primary_key = True)
    name = db.Column (db.String(length = 20) , nullable = False , unique = True)
    price = db.Column (db.Integer() , nullable = False)
    description = db.Column (db.String(length = 200) , nullable = False)

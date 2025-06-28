from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import datetime
db = SQLAlchemy()
#for authentication
class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username =db.Column(db.String(40))
    email =db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    payment_address = db.Column(db.String(100), nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    #----------------------------------raisa------------------------------
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer)





class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
#--------------------------------------------------package and venue model----------------------

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False) 

    # Establishing a relationship with packages
    package = db.relationship('Package', backref=db.backref('venues', lazy=True))


#----------------------------------------------end packaage and venue--------------------------------------------
  
#for booking slot
class Customer(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    date = db.Column(db.String(50))
    package = db.Column(db.String(50))
    number = db.Column(db.String(50))
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
    payment = db.relationship('Payment', backref='customer', uselist=False)


class Contacts(db.Model):
    contact_id= db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

    email =db.Column(db.String(50))
    
    description=db.Column(db.String(300))
    pnum =db.Column(db.String(15))



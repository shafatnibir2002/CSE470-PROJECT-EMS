from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import stripe
import os
from datetime import datetime
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from werkzeug.utils import secure_filename
import datetime


#database connection
local_server = True
app = Flask(__name__)
app.secret_key ="ghhjgdhghvhjfyuf"



#unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/event'

db=SQLAlchemy(app)

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



@app.route("/")
def index():
   
    return render_template("index.html")


#--------------------------------------contact start---------------------------------------------
@app.route("/contact",methods=['POST','GET'])
@login_required
def contact():
     if request.method =='POST':

        name=request.form.get('name')
        email=request.form.get('email')
        
        description=request.form.get("description")
        pnum=request.form.get("pnum")
        query=db.engine.execute(f"INSERT INTO `contact`(`name`,`email`,`description`,`pnum`)Values('{name}','{email}','{description}','{pnum}')")

        flash("We will get back to you soon","info")




     return render_template("contact.html")

#--------------------------------------contact finished---------------------------------------------
#-----------------------------------------------------------------------------------------------
#------------------------------------- booking form start---------------------------------------------

@app.route("/customer",methods=['POST','GET'])
@login_required
def Cust():
    if request.method =='POST':
        
        email=request.form.get('email')
        name=request.form.get('name')
        gender=request.form.get("gender")
        
        date=request.form.get("date")
        package=request.form.get("package")
        number=request.form.get("number")
        query=db.engine.execute(f"INSERT INTO `customer`(`email`,`name`,`date`,`package`,`number`)Values('{email}','{name}','{date}','{package}','{number}')")

        flash("booking confirmed","info")
    return render_template("customer.html")

#-------------------------------------- booking form finished---------------------------------------------

@app.route("/booking")
@login_required
def booking():
    em=current_user.email
    query=db.engine.execute(f"SELECT * FROM `customer` where email='{em}'")
    return render_template("booking.html",query=query)





@app.route("/edit/<string:cid>",methods=['POST','GET'])
@login_required
def edit(cid):
    posts=Customer.query.filter_by(cid=cid).first()
    if request.method =='POST':
        
        email=request.form.get('email')
        name=request.form.get('name')
        date=request.form.get("date")
        package=request.form.get("package")
        number=request.form.get("number")
        db.engine.execute(f"UPDATE `customer` SET `email`='{email}',`name`='{name}',`date`='{date}',`package`='{package}',`number`='{number}'WHERE `customer`.`cid`={cid}")
        flash("Slot is updated","success")
        return redirect("/booking")


    return render_template('edit.html',posts=posts)


@app.route("/delete/<string:cid>",methods=['POST','GET'])
@login_required
def delete(cid):
    db.engine.execute(f"DELETE FROM `customer` WHERE `customer`.`cid`={cid}")
    flash("Slot deleted successfully","danger")
    return redirect("/booking")


#-----------------------signup start------------------------------------------------------
@app.route("/signup",methods=['POST','GET'])
def signup():
    if request.method =='POST':
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template("/signup.html")
        
        encpassword= generate_password_hash(password)

        # fist method to insert in db
        #new_user = db.engine.execute(f"INSERT INTO `user`(`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}');")

        # second method to insert in db
        newuser =User(username=username,email=email,password=encpassword)
        db.session.add(newuser)
        db.session.commit()
        flash("Signup Success Please Login","success")
        return render_template("login.html")

    return render_template("signup.html")

#--------------------------------------signup finished---------------------------------------------


#--------------------------------------login start---------------------------------------------

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method =='POST':
        
        email=request.form.get('email')
        password=request.form.get('password')
        user= User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template("login.html")
    return render_template("login.html")

#--------------------------------------login finished---------------------------------------------
#---------------------------------sprint 2------------------------------------------------------------------
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/file")
def file():
    return render_template("file.html")



#--------------------------------------sprint2 end---------------------------------------------

#--------------------------------------logout---------------------------------------------
@app.route("/logout")
@login_required 
def logout():
    logout_user()
    flash("Logout Successful","warning")
    return redirect(url_for("login"))

#--------------------------------------logout finished---------------------------------------------
@app.route("/about")
def about():
    
    
    return render_template("about.html")


@app.route("/food") 
@login_required
def food():
    return render_template("food.html")

app.route("/offer") 
@login_required
def offer():
    return render_template("offer.html")




@app.route("/party")
@login_required 
def party():
    return render_template("party.html")


#----------------------------------raisa 
@app.route("/combooffer")
def combo_offer():
    return render_template("combooffer.html")


@app.route("/offer")
def offer():
    return render_template("offer.html")


@app.route("/seasonaldiscount")
def seasonal_discount():
    return render_template("seasonaldiscount.html")

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        comment_text = request.form['comment']
        
        comment = Comment(text=comment_text)
        db.session.add(comment)
        db.session.commit()
        
        flash('Comment submitted successfully!', 'success')
    
    comments = Comment.query.all()
    return render_template('review.html', comments=comments)

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    comment_text = request.form['comment']
    
    comment = Comment(text=comment_text)
    db.session.add(comment)
    db.session.commit()
    
    flash('Comment submitted successfully!', 'success')
    return redirect(url_for('review'))











@app.route("/rating")
def rating():
    
    has_rated = False 
    return render_template("rating.html", has_rated=has_rated)

@app.route("/submit_rating", methods=['POST'])
def submit_rating():
    rating_value = int(request.form.get('rating'))
    
   
    has_rated = True 
    
    if has_rated:
        rating_entry = Rating(rating=rating_value)
        
        db.session.add(rating_entry)
        db.session.commit()
        flash(f'{rating_value} rated!', 'success')
        
        

    #else:
        #flash("You've already rated.", 'error')
    
    return redirect(url_for('rating'))  


@app.route("/photo")
def photo():
    return render_template("photo.html")


@app.route("/package")
def package():
    packages = Package.query.all()
    return render_template('package.html', packages=packages)

@app.route('/admin/package', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_package = Package(name=name, description=description)
        db.session.add(new_package)
        db.session.commit()
        return redirect(url_for('admin_panel'))

    packages = Package.query.all()
    return render_template('admin.html', packages=packages)

#----------------delete and edit  package  ---------
@app.route('/admin/edit/package/<int:package_id>', methods=['GET', 'POST'])
def edit_package(package_id):
    package = Package.query.get_or_404(package_id)
    
    if request.method == 'POST':
        package.name = request.form['name']
        package.description = request.form['description']
        db.session.commit()
        return redirect(url_for('admin_panel'))
    
    return render_template('edit_package.html', package=package)

@app.route('/admin/delete/package/<int:package_id>', methods=['POST'])
def delete_package(package_id):
    package = Package.query.get_or_404(package_id)
    db.session.delete(package)
    db.session.commit()
    return redirect(url_for('admin_panel'))

# Admin Venue Management
@app.route('/admin/venue', methods=['GET', 'POST'])

def admin_venue():
    if request.method == 'POST':
        name = request.form['venue_name']
        price = float(request.form['venue_price'])
        description = request.form['venue_description']
        parent_package_id = int(request.form['parent_package'])

        new_venue = Venue(name=name, price=price, description=description, package_id=parent_package_id)
        db.session.add(new_venue)
        db.session.commit()
        flash("Venue added successfully", "success")
        return redirect(url_for('admin_venue'))
    else:
       venues = Venue.query.all()
       packages = Package.query.all()  # Retrieve all packages for the dropdown
       return render_template('admin_venue.html', venues=venues, packages=packages)

# Edit Venue
@app.route('/admin/edit/venue/<int:venue_id>', methods=['GET', 'POST'])

def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    
    if request.method == 'POST':
        venue.name = request.form['venue_name']
        venue.price = float(request.form['venue_price'])
        venue.description = request.form['venue_description']
        venue.package_id = int(request.form['parent_package'])
        
        db.session.commit()
        flash("Venue updated successfully", "info")
        return redirect(url_for('admin_venue'))

    packages = Package.query.all()  # Retrieve all packages for the dropdown
    return render_template('edit_venue.html', venue=venue, packages=packages)

# Delete Venue
@app.route('/admin/delete/venue/<int:venue_id>', methods=['POST'])

def delete_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    db.session.delete(venue)
    db.session.commit()
    flash("Venue deleted successfully", "danger")
    return redirect(url_for('admin_venue'))



@app.route("/faq")
def faq():
    return render_template("faq.html")




# @app.route("/venue")
# def venue():
#     return render_template("venue.html")


# add to cart 
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    package_name = request.form.get('package_name')
    package_price = float(request.form.get('package_price'))
    
    if 'cart' not in session:
        session['cart'] = []
    
    cart = session['cart']
    cart.append({'name': package_name, 'price': package_price})
    
    flash(f'{package_name} added to cart', 'info')
    return redirect(request.referrer)

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)
# remove from cart
@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):
    cart = session.get('cart', [])
    
    if 0 <= index < len(cart):
        removed_item = cart.pop(index)
        flash(f'{removed_item["name"]} removed from cart', 'danger')
    
    session['cart'] = cart
    return redirect(url_for('view_cart'))

@app.route('/details/<int:package_id>')
def package_details(package_id):
    package = Package.query.get_or_404(package_id)
    return render_template('package_details.html', package=package)


@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    package_name = request.form.get('package_name')
    package_price = float(request.form.get('package_price'))
    
    if 'wishlist' not in session:
        session['wishlist'] = []
    
    wishlist = session['wishlist']
    wishlist.append({'name': package_name, 'price': package_price})
    
    flash(f'{package_name} added to wishlist', 'success')
    return redirect(request.referrer)

@app.route('/wishlist')
def view_wishlist():
    wishlist = session.get('wishlist', [])
    return render_template('wishlist.html', wishlist=wishlist)

@app.route('/remove_from_wishlist/<int:index>')
def remove_from_wishlist(index):
    wishlist = session.get('wishlist', [])
    
    if 0 <= index < len(wishlist):
        removed_item = wishlist.pop(index)
        flash(f'{removed_item["name"]} removed from wishlist', 'danger')
    
    session['wishlist'] = wishlist
    return redirect(url_for('view_wishlist'))





#----------------------

@app.route('/search')
def search_packages():
    search_query = request.args.get('q', '')

   
    search_results = Package.query.filter(Package.name.ilike(f"%{search_query}%")).all()

    return render_template('search_results.html', search_results=search_results)
#---------------------------------------------------------------------------------------------Raisa

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', [])
    total_price = sum(item['price'] for item in cart)
    
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        package = request.form.get('package')
        number = request.form.get('number')
        payment_address = request.form.get('payment_address')
        payment_amount = float(request.form.get('payment_amount'))
        
        em = current_user.email
        new_booking = Customer(email=em, name=name, date=date, package=package, number=number)
        db.session.add(new_booking)
        
        new_payment = Payment(user_id=current_user.id, payment_address=payment_address, payment_amount=payment_amount)
        db.session.add(new_payment)
        
        db.session.commit()
        
        flash('Booking and payment successful! Your booking has been confirmed.', 'success')
        session['cart'] = []
        return redirect('/booking')

    return render_template('checkout.html', cart=cart, total_price=total_price)

    
@app.route('/order_details')
def admin_details():

   
    customers = Customer.query.all()
    payments= Payment.query.all()
    return render_template('order_details.html', customers=customers,payments=payments)

# @app.route('/delete/order/<int:cid>', methods=['POST'])
# def delete_order(cid):
#     customer = Customer.query.get_or_404(cid)

    
#     payment = Payment.query.get_or_404(customer.id)
#     db.session.delete(payment)
    
#     db.session.delete(customer)
#     db.session.commit()
    
#     return redirect('/order_details')

app.run(debug=True)
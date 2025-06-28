from flask import session, flash, redirect, url_for, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from models import User, Package, Payment, Comment, Contacts, Customer, Rating, Venue
from flask_login import login_user, logout_user, login_manager, LoginManager
from models import db
from flask_login import login_required, current_user

login_manager = LoginManager()


class UserController:
    def __init__(self, db):
        self.db = db

    def index(self):
        return render_template('index.html')

    def signup(self):
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()

            if user:
                flash("Email Already Exist", "warning")
                return render_template("/signup.html")

            encpassword = generate_password_hash(password)

            newuser = User(username=username, email=email, password=encpassword)
            db.session.add(newuser)
            db.session.commit()

            flash("Signup Success Please Login", "success")
            return render_template("login.html")

        return render_template("signup.html")

    def login(self):
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash("Login Success", "primary")
                return redirect(url_for('index'))
            else:
                flash("invalid credentials", "danger")
                return render_template("login.html")
        return render_template("login.html")

    def logout(self):
        logout_user()
        flash("Logout Successful", "warning")
        return redirect(url_for("login"))


class OtherController:
    def __init__(self, db):
        self.db = db

    def gallery(self):
        return render_template("gallery.html")

    def file(self):
        return render_template("file.html")

    def about(self):
        return render_template("about.html")

    def offer(self):
        return render_template("offer.html")

    def combo_offer(self):
        return render_template("combooffer.html")

    def seasonal_discount(self):
        return render_template("seasonaldiscount.html")

    def review(self):
        if request.method == 'POST':
            comment_text = request.form['comment']
            comment = Comment(text=comment_text)
            db.session.add(comment)
            db.session.commit()
            flash('Comment submitted successfully!', 'success')

        comments = Comment.query.all()
        return render_template('review.html', comments=comments)

    def submit_comment(self):
        comment_text = request.form['comment']
        comment = Comment(text=comment_text)
        db.session.add(comment)
        db.session.commit()
        flash('Comment submitted successfully!', 'success')
        return redirect(url_for('review'))

    def rating(self):
        has_rated = False
        return render_template("rating.html", has_rated=has_rated)

    def submit_rating(self):
        rating_value = int(request.form.get('rating'))
        has_rated = True

        if has_rated:
            rating_entry = Rating(rating=rating_value)
            db.session.add(rating_entry)
            db.session.commit()
            flash(f'{rating_value} rated!', 'success')

        return redirect(url_for('rating'))

    def photo(self):
        return render_template("photo.html")


class PackageController:
    def __init__(self, db):
        self.db = db

    def package(self):
        packages = Package.query.all()
        return render_template('package.html', packages=packages)

    def admin_panel(self):
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            new_package = Package(name=name, description=description)
            db.session.add(new_package)
            db.session.commit()
            return redirect(url_for('admin_panel'))

        packages = Package.query.all()
        return render_template('admin.html', packages=packages)

    def edit_package(self, package_id):
        package = Package.query.get_or_404(package_id)

        if request.method == 'POST':
            package.name = request.form['name']
            package.description = request.form['description']
            db.session.commit()
            return redirect(url_for('admin_panel'))

        return render_template('edit_package.html', package=package)

    def delete_package(self, package_id):
        package = Package.query.get_or_404(package_id)
        db.session.delete(package)
        db.session.commit()
        return redirect(url_for('admin_panel'))

    def admin_venue(self):
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
            packages = Package.query.all()
            return render_template('admin_venue.html', venues=venues, packages=packages)

    def edit_venue(self, venue_id):
        venue = Venue.query.get_or_404(venue_id)

        if request.method == 'POST':
            venue.name = request.form['venue_name']
            venue.price = float(request.form['venue_price'])
            venue.description = request.form['venue_description']
            venue.package_id = int(request.form['parent_package'])

            db.session.commit()
            flash("Venue updated successfully", "info")
            return redirect(url_for('admin_venue'))

        packages = Package.query.all()
        return render_template('edit_venue.html', venue=venue, packages=packages)

    def delete_venue(self, venue_id):
        venue = Venue.query.get_or_404(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash("Venue deleted successfully", "danger")
        return redirect(url_for('admin_venue'))

    def faq(self):
        return render_template("faq.html")
    
    #for see the venue packages
    def package_details(self,package_id):
        package = Package.query.get_or_404(package_id)
        return render_template('package_details.html', package=package)

class CartController:
    def __init__(self,db):
        self.db = db

    def add_to_cart(self):
        package_name = request.form.get('package_name')
        package_price = float(request.form.get('package_price'))

        if 'cart' not in session:
            session['cart'] = []

        cart = session['cart']
        cart.append({'name': package_name, 'price': package_price})

        flash(f'{package_name} added to cart', 'info')
        return redirect(request.referrer)

    def view_cart(self):
        cart = session.get('cart', [])
        return render_template('cart.html', cart=cart)

    def remove_from_cart(self, index):
        cart = session.get('cart', [])

        if 0 <= index < len(cart):
            removed_item = cart.pop(index)
            flash(f'{removed_item["name"]} removed from cart', 'danger')

        session['cart'] = cart
        return redirect(url_for('view_cart'))
#     @pp.route('/details/<int:package_id>')
    


    #@app.route('/add_to_wishlist', methods=['POST'])
    def add_to_wishlist(self):
        package_name = request.form.get('package_name')
        package_price = float(request.form.get('package_price'))
        
        if 'wishlist' not in session:
            session['wishlist'] = []
        
        wishlist = session['wishlist']
        wishlist.append({'name': package_name, 'price': package_price})
        
        flash(f'{package_name} added to wishlist', 'success')
        return redirect(request.referrer)

    #@app.route('/wishlist')
    def view_wishlist(self):
        wishlist = session.get('wishlist', [])
        return render_template('wishlist.html', wishlist=wishlist)

    #@app.route('/remove_from_wishlist/<int:index>')
    def remove_from_wishlist(self,index):
        wishlist = session.get('wishlist', [])
        
        if 0 <= index < len(wishlist):
            removed_item = wishlist.pop(index)
            flash(f'{removed_item["name"]} removed from wishlist', 'danger')
        
        session['wishlist'] = wishlist
        return redirect(url_for('view_wishlist'))





#----------------------
class AdditionalController:
    def __init__(self, db):
        self.db = db

   #--------------------------------------contact start---------------------------------------------
    #@app.route("/contact",methods=['POST','GET'])
    @login_required
    def contact(self):
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

    #@app.route("/customer",methods=['POST','GET'])
    @login_required
    def Cust(self):
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

    #@app.route("/booking")
    @login_required
    def booking(self):
        em=current_user.email
        query=db.engine.execute(f"SELECT * FROM `customer` where email='{em}'")
        return render_template("booking.html",query=query)





    #@app.route("/edit/<string:cid>",methods=['POST','GET'])
    @login_required
    def edit(self,cid):
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


    #@app.route("/delete/<string:cid>",methods=['POST','GET'])
    @login_required
    def delete(self,cid):
        db.engine.execute(f"DELETE FROM `customer` WHERE `customer`.`cid`={cid}")
        flash("Slot deleted successfully","danger")
        return redirect("/booking")


    def search_packages(self):
        search_query = request.args.get('q', '')
    
        search_results = Package.query.filter(Package.name.ilike(f"%{search_query}%")).all()

        return render_template('search_results.html', search_results=search_results)
    #---------------------------------------------------------------------------------------------Raisa

    #@app.route('/checkout', methods=['GET', 'POST'])
    @login_required
    def checkout(self):
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

        
    #@app.route('/order_details')
    def admin_details(self):

    
        customers = Customer.query.all()
        payments= Payment.query.all()
        return render_template('order_details.html', customers=customers,payments=payments)
    def package_details(self,package_id):
        package = Package.query.get_or_404(package_id)
        return render_template('package_details.html', package=package)
    # def gallery(self):
    #     return render_template("gallary.html")
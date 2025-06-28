from flask import Flask
from controllers import UserController, OtherController, PackageController, CartController,AdditionalController
from models import db,User
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjkjkoiforejkfkrjkjvg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/event'
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Load the user_loader function from controllers
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize controllers
user_controller = UserController(db)
other_controller = OtherController(db)
package_controller = PackageController(db)
cart_controller = CartController(db)
additional_controller= AdditionalController(db)
# Define routes
app.add_url_rule('/', 'index', user_controller.index)
app.add_url_rule('/signup', 'signup', user_controller.signup, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', user_controller.login, methods=['GET', 'POST'])
app.add_url_rule('/logout', 'logout', user_controller.logout)
app.add_url_rule('/gallery', 'gallery', other_controller.gallery)
app.add_url_rule('/file', 'file', other_controller.file)
app.add_url_rule('/about', 'about', other_controller.about)
app.add_url_rule('/offer', 'offer', other_controller.offer)
app.add_url_rule('/combooffer', 'combo_offer', other_controller.combo_offer)
app.add_url_rule('/seasonaldiscount', 'seasonal_discount', other_controller.seasonal_discount)
app.add_url_rule('/review', 'review', other_controller.review, methods=['GET', 'POST'])
app.add_url_rule('/submit_comment', 'submit_comment', other_controller.submit_comment, methods=['POST'])
app.add_url_rule('/rating', 'rating', other_controller.rating)
app.add_url_rule('/submit_rating', 'submit_rating', other_controller.submit_rating, methods=['POST'])
app.add_url_rule('/photo', 'photo', other_controller.photo)
app.add_url_rule('/package', 'package', package_controller.package)
app.add_url_rule('/details/<int:package_id>', 'package_details', package_controller.package_details)
app.add_url_rule('/admin/package', 'admin_panel', package_controller.admin_panel, methods=['GET', 'POST'])
app.add_url_rule('/admin/edit/package/<int:package_id>', 'edit_package', package_controller.edit_package, methods=['GET', 'POST'])
app.add_url_rule('/admin/delete/package/<int:package_id>', 'delete_package', package_controller.delete_package, methods=['POST'])
app.add_url_rule('/admin/venue', 'admin_venue', package_controller.admin_venue, methods=['GET', 'POST'])
app.add_url_rule('/admin/edit/venue/<int:venue_id>', 'edit_venue', package_controller.edit_venue, methods=['GET', 'POST'])
app.add_url_rule('/admin/delete/venue/<int:venue_id>', 'delete_venue', package_controller.delete_venue, methods=['POST'])
app.add_url_rule('/faq', 'faq', package_controller.faq)
app.add_url_rule('/add_to_cart', 'add_to_cart', cart_controller.add_to_cart, methods=['POST'])
app.add_url_rule('/cart', 'view_cart', cart_controller.view_cart)
app.add_url_rule('/remove_from_cart/<int:index>', 'remove_from_cart', cart_controller.remove_from_cart, methods=['POST'])


app.add_url_rule('/add_to_wishlist', 'add_to_wishlist', cart_controller.add_to_wishlist, methods=['POST'])
app.add_url_rule('/wishlist', 'view_wishlist', cart_controller.view_wishlist)
app.add_url_rule('/remove_from_wishlist/<int:index>', 'remove_from_wishlist', cart_controller.remove_from_wishlist, methods=['POST'])


app.add_url_rule('/search', 'search_packages', additional_controller.search_packages)
app.add_url_rule('/checkout', 'checkout', additional_controller.checkout, methods=['GET','POST'])
app.add_url_rule('/order_details', 'admin_details',additional_controller.admin_details)
app.add_url_rule('/contact', 'contact',additional_controller.contact, methods=['GET', 'POST'])
app.add_url_rule('/customer', 'Cust',additional_controller.Cust, methods=['GET', 'POST'])
app.add_url_rule('/booking', 'booking',additional_controller.booking)
app.add_url_rule('/edit/<string:cid>', 'edit',additional_controller.edit, methods=['GET', 'POST'])
app.add_url_rule('/delete/<string:cid>', 'delete',additional_controller.delete,methods=['GET', 'POST'])
#app.add_url_rule('/gallery', 'gallery',additional_controller.gallery)







if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask,current_app, Blueprint
from database import db,ma,migrate,redis_cache
from flask_migrate import Migrate
from auth.auth_api import auth_blueprint
from product.product_api import product_blueprint
from category.category_api import category_blueprint
from wishlist.wishlist_api import wishlist_blueprint
from cart.cart_api import cart_blueprint
from order.order_api import order_blueprint



# def create_app():
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
# os.getenv('DB_USER', 'flask'),
# os.getenv('DB_PASSWORD', ''),
# os.getenv('DB_HOST', 'mysql'),
# os.getenv('DB_NAME', 'flask')
# )      


#--------------------APP CONFIG-------------------#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:suvarna123@localhost:3306/ecommdb'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:////home/neosoft-suvarna/Desktop/Flask_Ecomm_Api/Ecomm_Backend/ecommdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



#--------------REDIS CACHE CONFIG--------------#
app.config["REDIS_HOST"] = "localhost"
app.config["REDIS_PASSWORD"] = "password"
app.config["REDIS_PORT"] = 6379


os.environ['SECRET_KEY'] = 'secret'

#-----------BLUEPRINT REGISTRATION-------------#
app.register_blueprint(auth_blueprint)
app.register_blueprint(product_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(wishlist_blueprint)
app.register_blueprint(cart_blueprint)
app.register_blueprint(order_blueprint)


ma.init_app(app)
db.init_app(app)
redis_cache.init_app(app)
migrate.init_app(app, db)
# migrate = Migrate(app, db)

# return app


@app.before_first_request
def create_tables():
    db.create_all()

# if __name__ == "main":
#     create_app()


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)


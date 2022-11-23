from sqlalchemy import DateTime, ForeignKey
from database import db,ma
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50),unique=True,)
    full_name = db.Column(db.String(100))
    password = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean)
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = db.Column(DateTime, default=datetime.datetime.utcnow,onupdate=datetime)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    category = db.Column(db.Integer,ForeignKey("category.id"))
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = db.Column(DateTime, default=datetime.datetime.utcnow,onupdate=datetime)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey("user.id"))   
    order_amount = db.Column(db.Integer)
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    updated_date = db.Column(DateTime, default=datetime.datetime.utcnow,onupdate=datetime)


class OrdertoProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,ForeignKey("order.id"))
    product_id = db.Column(db.Integer,ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)

        
class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey("user.id"))
    product_id = db.Column(db.Integer,ForeignKey("product.id"))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,ForeignKey("user.id"))
    product_id = db.Column(db.Integer,ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        include_relationships = True
        fields = ('id', 'category')

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_relationships = True
        fields = ('id', 'product_name','price')    

class WishlistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wishlist
        load_instance = True
        include_relationships = True
        fields = ('id', 'user_id','product_id')
 

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True
        fields = ('id','email','full_name', 'password', 'is_admin')


class OrdertoProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrdertoProduct
        load_instance = True
        include_relationships = True
        fields = ('id','order_id','products')

    products = ma.Nested(ProductSchema, many=True)
import datetime
from functools import wraps
import os
import uuid
from flask import Blueprint, jsonify,request,make_response
from database import db
from models import Product, ProductSchema, User,Cart
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

cart_blueprint = Blueprint('cart_blueprint', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers)

        if 'X-Access-Token' in request.headers:
            token = request.headers['x-access-token']
            print('token :', token)

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            print("data:", data)
            current_user = User.query.filter_by(email=data['email']).first()
            print("current_user", current_user.email)
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@cart_blueprint.route('/cart/<user_id>', methods=['POST'])
@token_required
def add_to_cart(current_user,user_id):  
    data = request.get_json()
    item = Cart(user_id=user_id, product_id=data['product_id'],quantity=data['quantity'])
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Added To Cart !'})


@cart_blueprint.route('/cart/<user_id>')
@token_required
def get_cart_product(current_user,user_id):
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    products = []
    for item in cart_items:
        product = Product.query.filter_by(id=item.product_id).first()
        product_schema = ProductSchema()
        output = product_schema.dump(product)
        products.append({
            "productInfo":output,
            "quantity":item.quantity
        })

    return jsonify({'cart': products})


@cart_blueprint.route('/cart/<user_id>', methods=['DELETE'])
@token_required
def remove_from_cart(current_user, user_id):
    data = request.get_json()
    cart_items = Cart.query.filter_by(user_id=user_id,product_id=data['product_id']).first()
    if not cart_items:
        return jsonify({'message': 'No item found!'})
    db.session.delete(cart_items)
    db.session.commit()

    return jsonify({'message': 'The product has been removed!'})


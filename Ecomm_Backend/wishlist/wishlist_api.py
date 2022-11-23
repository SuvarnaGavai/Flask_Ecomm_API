import datetime
from functools import wraps
import os
import uuid
from flask import Blueprint, jsonify,request,make_response
from database import db
from models import Category, Product, ProductSchema, User, Wishlist
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

wishlist_blueprint = Blueprint('wishlist_blueprint', __name__)

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


@wishlist_blueprint.route('/add_wishlist', methods=['POST'])
@token_required
def add_to_wishlist(current_user):  
    data = request.get_json()
    product = Wishlist( user_id=data['user_id'],product_id=data['product_id'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product Added In Wishlist!'})


@wishlist_blueprint.route('/wishlist/<user_id>')
@token_required
def get_wishlist(current_user,user_id):  
    wishlist = Wishlist.query.filter_by(user_id = user_id).all()
    products = []
    for item in wishlist:
        product = Product.query.filter_by(id=item.product_id).first()
        products.append(product)

    product_schema = ProductSchema(many=True)
    output = product_schema.dump(products)

    return jsonify({'products': output})

@wishlist_blueprint.route('/wishlist/<user_id>', methods=['DELETE'])
@token_required
def remove_wishlist_product(current_user, user_id):
    data = request.get_json()
    item = Wishlist.query.filter_by(user_id=user_id, product_id=data['product_id']).first()

    if not item:
        return jsonify({'message': 'No user found!'})

    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'The product has been deleted!'})

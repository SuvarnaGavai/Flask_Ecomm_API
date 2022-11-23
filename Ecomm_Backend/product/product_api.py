from ast import literal_eval
import datetime
from functools import wraps
import os
import uuid
from flask import Blueprint, jsonify,request,make_response
from database import db
from models import Category, Product, ProductSchema, User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from database import redis_cache
from constants import PRODUCTS_LIST

product_blueprint = Blueprint('product_blueprint', __name__)

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


@product_blueprint.route('/product', methods=['POST'])
@token_required
def create_product(current_user):  
    if not current_user.is_admin:
        return jsonify({'message': 'Cannot perform that function!'})
    data = request.get_json()
    new_product = Product( product_name=data['productName'],price=data['price'],category=data['category_id'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product Added Successfully!'})


@product_blueprint.route('/product', methods=['GET'])
@token_required
def get_all_product(current_user): 
    product_schema = ProductSchema(many=True) 
    if redis_cache.exists(PRODUCTS_LIST):      
        products = redis_cache.get(PRODUCTS_LIST)
        products = literal_eval(products.decode('utf8'))
        output = product_schema.dump(products)
        print("if")
    else:
        products = Product.query.all()
        output = product_schema.dump(products)
        products = str(output)
        redis_cache.set(PRODUCTS_LIST, products)
        print("else")

    # output = product_schema.dump(products)
    return jsonify({'products': output})


@product_blueprint.route('/product/<product_id>', methods=['GET'])
@token_required
def get_one_product(current_user,product_id):  
    products = Product.query.filter_by(id=product_id).first()
    product_schema = ProductSchema()
    output = product_schema.dump(products)

    return jsonify({'product': output})


@product_blueprint.route('/product/category/<category_id>', methods=['GET'])
@token_required
def get_category_product(current_user,category_id):  
    products = Product.query.filter_by(category=category_id).all()
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(products)

    return jsonify({'products': output})


@product_blueprint.route('/product/<id>', methods=['DELETE'])
@token_required
def delete_product(current_user, id):
    if not current_user.is_admin:
        return jsonify({'message': 'User is Not Admin !! Cannot perform that function!'})

    product = Product.query.filter_by(id=id).first()

    if not product:
        return jsonify({'message': 'No user found!'})

    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'The product has been deleted!'})


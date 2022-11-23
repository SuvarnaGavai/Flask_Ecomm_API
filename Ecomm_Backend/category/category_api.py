from ast import literal_eval
from functools import wraps
import os
from flask import Blueprint, jsonify,request
from constants import CATEGORY_LIST
from database import db, redis_cache
from models import Category, CategorySchema, User
import jwt
from constants import PRODUCTS_LIST

category_blueprint = Blueprint('category_blueprint', __name__)

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


@category_blueprint.route('/category', methods=['POST'])
@token_required
def create_category(current_user):  
    if not current_user.is_admin:
        return jsonify({'message': 'Cannot perform that function!'})
    data = request.get_json()
    new_category = Category( category=data['category'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category Created Successfully!'})


@category_blueprint.route('/category', methods=['GET'])
@token_required
def get_all_category(current_user):   
    category_schema = CategorySchema(many=True) 
    if redis_cache.exists(CATEGORY_LIST):      
        categories = redis_cache.get(CATEGORY_LIST)
        categories = literal_eval(categories.decode('utf8'))
        output = category_schema.dump(categories)
        print("if")

    else:
        categories = Category.query.all()
        output = category_schema.dump(categories)
        categories = str(output)
        redis_cache.set(CATEGORY_LIST, categories)
        print("else")

    return jsonify({'categories': output})


@category_blueprint.route('/category/<id>', methods=['DELETE'])
@token_required
def delete_category(current_user, id):
    if not current_user.is_admin:
        return jsonify({'message': 'User is Not Admin !! Cannot perform that function!'})

    category = Category.query.filter_by(id=id).first()

    if not category:
        return jsonify({'message': 'No user found!'})

    db.session.delete(category)
    db.session.commit()

    return jsonify({'message': 'The category has been deleted!'})
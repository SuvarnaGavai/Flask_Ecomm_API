import datetime
from functools import wraps
import os
import uuid
from flask import Blueprint, jsonify,request,make_response
from database import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import jwt


auth_blueprint = Blueprint('auth_blueprint', __name__)


# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         print(request.headers)

#         if 'X-Access-Token' in request.headers:
#             token = request.headers['x-access-token']
#             print('token :', token)

#         if not token:
#             return jsonify({'message': 'Token is missing!'}), 401

#         try:
#             data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
#             print("data:", data)
#             current_user = User.query.filter_by(public_id=data['public_id']).first()
#             print("current_user", current_user.username)
#         except:
#             return jsonify({'message': 'Token is invalid!'}), 401

#         return f(current_user, *args, **kwargs)

#     return decorated


@auth_blueprint.route('/signup', methods=['POST'])
def signup_user():  
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    print(hashed_password)
    new_user = User(email=data['email'],full_name=data['fullname'], password=hashed_password,is_admin=data['is_admin'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User Registered Successfully!'})


@auth_blueprint.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})

    user = User.query.filter_by(email=auth.username).first()
    print("Emai :",user.email)
    print("Username : ",auth.username)
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'email': user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},os.getenv('SECRET_KEY'))
        print(user.email)
        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Login required!'})

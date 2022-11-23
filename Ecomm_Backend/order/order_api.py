from functools import wraps
import os
from flask import Blueprint, jsonify,request,make_response
from database import db
from models import Order, OrdertoProduct, OrdertoProductSchema, Product, ProductSchema, User,Cart
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

order_blueprint = Blueprint('order_blueprint', __name__)

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


@order_blueprint.route('/order/<user_id>',methods=['POST'])
@token_required
def order(current_user,user_id):
    items = Cart.query.filter_by(user_id=user_id).all()
    total_price = 0
    
    for item in items:
         product = Product.query.filter_by(id=item.product_id).first()
         total_price += product.price * item.quantity
    
    order = Order(user_id=user_id,order_amount=total_price)
    db.session.add(order)
    db.session.flush()
    for item in items:
        entry = OrdertoProduct(order_id=order.id,product_id=item.product_id,quantity=item.quantity)
        db.session.add(entry)
    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({'message': 'Order Placed Successfully !!!'})


@order_blueprint.route('/order')
@token_required
def get_orders(current_user):
    if not current_user.is_admin:
        return jsonify({'message': 'User is Not Admin !! Cannot perform that function!'})

    orders = Order.query.all()
    final_list = []
    for order in orders:
        product_id_list = db.session.query(OrdertoProduct.product_id).filter(OrdertoProduct.order_id ==order.id).all()
        id_list = [item for t in product_id_list for item in t]
        product_list = db.session.query(Product).filter(Product.id.in_(id_list)).all()
        product_schema = ProductSchema(many=True)
        output = product_schema.dump(product_list)
        final_list.append({
            "id": order.id,
            "user_id":order.user_id,
            "order_amount":order.order_amount,
            "product_details":output
        })
    return jsonify({'orders': final_list})


@order_blueprint.route('/order/<user_id>')
@token_required
def get_one_order(current_user,user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    final_list = []
    if len(orders) > 0:
        for order in orders:
            product_id_list = db.session.query(OrdertoProduct.product_id).filter(OrdertoProduct.order_id ==order.id).all()
            id_list = [item for t in product_id_list for item in t]
            product_list = db.session.query(Product).filter(Product.id.in_(id_list)).all()
            product_schema = ProductSchema(many=True)
            output = product_schema.dump(product_list)
            final_list.append({
                "id": order.id,
                "user_id":order.user_id,
                "order_amount":order.order_amount,
                "product_details":output
            })
        return jsonify({'orders': final_list})
    
    return jsonify({'message': "No Order Found"})


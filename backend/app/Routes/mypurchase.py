from flask import request
from app import app
from app.models import Product, Order, OrderStatus, Shop, Color, Size, Rating
from flask_login import login_required, current_user
from app.Components.response import Response

@login_required
@app.route('/api/v1/mypurchase', methods=['GET'])
def mypurchase():
    if current_user.userType == 'Seller':
        return Response(
            status=403,
            message="error",
        )
    
    if request.method == 'GET':
        orders = Order.query.order_by(Order.dateCreated.desc()).filter_by(user=current_user.id).all()

        products = []
        for order in orders:
            product = Product.query.get(order.product)
            status = OrderStatus.query.get(order.status)
            shop = Shop.query.get(product.shop)
            rating = Rating.query.filter_by(product=product.id,user=current_user.id).first()

            prod = product.to_dict(exclude=['description', 'shop', 'dateCreated', 'dateUpdated'])
            prod['category'] = product.cat.name
            prod['gender'] = product.gen.name
            prod['quantity'] = order.quantity
            prod['shop'] = shop.shopName
            prod['status'] = {'id': status.id, 'name': status.name}
            prod['fullname'] = order.fullname
            prod['number'] = order.number
            prod['address'] = order.address
            prod['dateCreated'] = order.dateCreated
            prod['orderID'] = order.id
            prod['total'] = order.quantity * product.price
            prod['color'] = Color.query.get(order.color).color
            prod['size'] = Size.query.get(order.size).size
            prod['rating'] = rating.rating if rating else 0

            products.append(prod)

        return Response(
            status=200,
            data=products
        )

@app.route('/api/v1/mypurchase/notification', methods=['GET'])
@login_required
def notification():
    if current_user.userType == 'Seller':
        return Response(
            status=403,
            message="error",
        )
    if request.method == 'GET':
        orders = Order.query.order_by(Order.dateCreated.desc()).filter_by(user=current_user.id).all()

        orderStatus = []
        for order in orders:
            status = OrderStatus.query.get(order.status)
            if status.name == "PREPARING":
                orderStatus.append(
                   { "order_id": order.id, "status": status.name}
                )
        
        return Response(
            status=200,
            data=orderStatus
        )
        
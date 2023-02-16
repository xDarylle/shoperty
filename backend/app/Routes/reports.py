from app import app, db
from flask_login import login_required, current_user
from flask import request
from app.Components.response import Response
from app.models import Order, Shop, Product, Sold, OrderStatus, User, Category
from datetime import datetime

DATES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

@login_required
@app.route('/api/v1/admin/reports', methods=['GET'])
def reports():
    if current_user.userType == 'Buyer':
        return Response(
            status=403,
            message="error",
        )

    if request.method == 'GET':
        shop = Shop.query.filter_by(user=current_user.id).first()
        products = Product.query.filter_by(shop=shop.id).all()
        orders = Order.query.order_by(Order.dateCreated.desc()).join(Product.query.filter_by(shop=shop.id)).all()
        solds = Sold.query.order_by(Sold.quantity.desc()).join(Product.query.filter_by(shop=shop.id)).all()

        totalSales = 0
        for order in orders:
            if order.status == OrderStatus.query.filter_by(name='COMPLETE').first().id:
                prod = Product.query.get(order.product)
                totalSales += prod.price * order.quantity
            
        latestOrders = []
        for i, order in enumerate(orders):
            if i < 5:
                detail = order.to_dict()
                detail['buyer'] = User.query.get(order.user).firstName +" "+User.query.get(order.user).lastName
                detail['product'] = Product.query.get(order.product).productName
                detail['price'] = Product.query.get(order.product).price * order.quantity
                detail['status'] = OrderStatus.query.get(order.status).name
                latestOrders.append(detail)

        sales = [{'date': date, 'sales': 0} for date in DATES]

        for order in orders:
            if order.status == OrderStatus.query.filter_by(name='COMPLETE').first().id:
                date = order.dateCreated.strftime('%b')
                product = Product.query.get(order.product)
                price = product.price * order.quantity
                for sale in sales:
                    if sale['date'] == date:
                        sale['sales'] += price

        categories = Category.query.filter_by(shop=shop.id).all()
        sales_by_category = [{'sales': 0, 'category': category.name} for category in categories]
        for order in orders:
            if order.status == OrderStatus.query.filter_by(name='COMPLETE').first().id:
                product = Product.query.get(order.product)
                price = product.price * order.quantity
                for sale in sales_by_category:
                    if sale['category'] == Category.query.get(product.category).name:
                        sale['sales'] += price

        topSelling = []
        for i, sold in enumerate(solds):
            if i < 10 and sold.quantity > 0:
                product = Product.query.get(sold.product)
                detail = product.to_dict()
                detail['quantity'] = sold.quantity
                topSelling.append(detail)

        data = {}
        data["totalSales"] = totalSales
        data['totalOrders'] = len(orders)
        data['totalProducts'] = len(products)
        data['latestOrders'] = latestOrders
        data['sales'] = sales
        data['sales_by_category'] = sales_by_category
        data['topSelling'] = topSelling

        return Response(
            data=data,
            status=200
        )





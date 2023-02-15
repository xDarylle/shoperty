from app import db
from sqlalchemy.sql import func
from app.Components import model

class Product(db.Model, model.Component):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    shop = db.Column(db.Integer, db.ForeignKey('shop.id'))
    productName = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False)

    gender = db.Column(db.Integer, db.ForeignKey('gender.id'), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    quantityStatus = db.relationship('QuantityStatus', backref='prod', lazy='joined')

    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())
    dateUpdated = db.Column(db.TIMESTAMP, onupdate=func.now())

class QuantityStatus(db.Model, model.Component):
    __tablename__ = 'quantity_status'

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    dateUpdated = db.Column(db.TIMESTAMP, onupdate=func.now())

class Category(db.Model, model.Component):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    shop = db.Column(db.Integer, db.ForeignKey('shop.id'))
    productID = db.relationship('Product', backref='cat', lazy='joined')

    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())
    dateUpdated = db.Column(db.TIMESTAMP, onupdate=func.now())

class Gender(db.Model, model.Component):
    __tablename__ = 'gender'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    product = db.relationship('Product', backref='gen', lazy='joined')

class Color(db.Model, model.Component):
    __tablename__ = 'color'

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    color = db.Column(db.String(64), nullable=False)

class Size(db.Model, model.Component):
    __tablename__ = 'size'

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    size = db.Column(db.String(10), nullable=False)

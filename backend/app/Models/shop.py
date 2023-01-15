from app import db
from sqlalchemy.sql import func
from app.Components import model

class Shop(db.Model, model.Component):
    __tablename__ = 'shop'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    shopName = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.Text, nullable=False)

    dateCreated = db.Column(db.TIMESTAMP, server_default=func.now())
    dateUpdated = db.Column(db.TIMESTAMP, onupdate=func.now())



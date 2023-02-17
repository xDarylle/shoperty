from app import db
from app.Components import model

class Rating(db.Model, model.Component):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('product.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    rating = db.Column(db.Integer, nullable=False)
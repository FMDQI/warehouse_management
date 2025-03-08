from models.db import db

class ReplenishmentOrder(db.Model):
    __tablename__ = 'replenishment_orders'
    order_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('normal_items.item_id'), nullable=False)
    order_quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('pending', 'completed'), default='pending')





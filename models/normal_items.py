from models.db import db

class NormalItem(db.Model):
    __tablename__ = 'normal_items'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255), nullable=False)
    item_type = db.Column(db.String(100), nullable=False)
    production_date = db.Column(db.Date, nullable=False)
    shelf_life = db.Column(db.Integer, nullable=False)
    inventory = db.relationship('Inventory', backref='normal_item', lazy=True)
    sales_records = db.relationship('SalesRecord', backref='normal_item', lazy=True)
    sales_predictions = db.relationship('SalesPrediction', backref='normal_item', lazy=True)
    replenishment_orders = db.relationship('ReplenishmentOrder', backref='normal_item', lazy=True)





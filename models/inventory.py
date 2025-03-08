from models.db import db

class Inventory(db.Model):
    __tablename__ = 'inventory'
    inventory_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('normal_items.item_id'), nullable=False)
    current_stock = db.Column(db.Integer, nullable=False)





from models.db import db

class SalesRecord(db.Model):
    __tablename__ = 'sales_records'
    sale_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('normal_items.item_id'), nullable=False)
    sale_quantity = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.Date, nullable=False)





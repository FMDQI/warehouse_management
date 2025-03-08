from models.db import db

class RecyclableItem(db.Model):
    __tablename__ = 'recyclable_items'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255), nullable=False)
    item_type = db.Column(db.String(100), nullable=False)
    recycling_records = db.relationship('RecyclingRecord', backref='recyclable_item', lazy=True)




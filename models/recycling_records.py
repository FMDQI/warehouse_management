from models.db import db

class RecyclingRecord(db.Model):
    __tablename__ = 'recycling_records'
    record_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('recyclable_items.item_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    recycle_date = db.Column(db.Date, nullable=False)





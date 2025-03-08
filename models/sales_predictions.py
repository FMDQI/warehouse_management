from models.db import db

class SalesPrediction(db.Model):
    __tablename__ = 'sales_predictions'
    prediction_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('normal_items.item_id'), nullable=False)
    predicted_sales = db.Column(db.Integer, nullable=False)
    prediction_date = db.Column(db.Date, nullable=False)





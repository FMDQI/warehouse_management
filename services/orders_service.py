from models.sales_records import SalesRecord
from models.db import db

def get_all_orders():
    """
    获取所有订单数据
    """
    orders = SalesRecord.query.all()
    return [{
        "sale_id": order.sale_id,
        "item_id": order.item_id,
        "sale_quantity": order.sale_quantity,
        "sale_date": order.sale_date
    } for order in orders]

def get_order_by_id(sale_id):
    """
    根据订单 ID 获取单个订单数据
    """
    order = SalesRecord.query.get(sale_id)
    if order:
        return {
            "sale_id": order.sale_id,
            "item_id": order.item_id,
            "sale_quantity": order.sale_quantity,
            "sale_date": order.sale_date
        }
    return None

def create_order(item_id, sale_quantity, sale_date):
    """
    创建新的订单记录
    """
    new_order = SalesRecord(item_id=item_id, sale_quantity=sale_quantity, sale_date=sale_date)
    db.session.add(new_order)
    db.session.commit()
    return {
        "sale_id": new_order.sale_id,
        "item_id": new_order.item_id,
        "sale_quantity": new_order.sale_quantity,
        "sale_date": new_order.sale_date
    }

def update_order(sale_id, item_id=None, sale_quantity=None, sale_date=None):
    """
    更新订单记录
    """
    order = SalesRecord.query.get(sale_id)
    if not order:
        return None

    if item_id is not None:
        order.item_id = item_id
    if sale_quantity is not None:
        order.sale_quantity = sale_quantity
    if sale_date is not None:
        order.sale_date = sale_date

    db.session.commit()
    return {
        "sale_id": order.sale_id,
        "item_id": order.item_id,
        "sale_quantity": order.sale_quantity,
        "sale_date": order.sale_date
    }

def delete_order(sale_id):
    """
    删除订单记录
    """
    order = SalesRecord.query.get(sale_id)
    if not order:
        return False

    db.session.delete(order)
    db.session.commit()
    return True




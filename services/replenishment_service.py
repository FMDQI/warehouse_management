from models.inventory import Inventory
from models.replenishment_orders import ReplenishmentOrder
from models.db import db
from datetime import datetime

def get_low_stock_items(threshold):
    """
    获取库存低于阈值的商品列表
    """
    low_stock_items = Inventory.query.filter(Inventory.current_stock < threshold).all()
    return [{
        "inventory_id": item.inventory_id,
        "item_id": item.item_id,
        "current_stock": item.current_stock
    } for item in low_stock_items]

def create_replenishment_order(item_id, order_quantity):
    """
    创建补货订单，而不是直接增加库存
    """
    item = Inventory.query.filter_by(item_id=item_id).one_or_none()
    
    if not item:
        return None, "商品不存在"

    # 避免重复创建订单
    existing_order = ReplenishmentOrder.query.filter_by(item_id=item_id, status="pending").first()
    if existing_order:
        return None, "已有待处理订单"

    new_order = ReplenishmentOrder(
        item_id=item_id,
        order_quantity=order_quantity,
        order_date=datetime.utcnow(),
        status="pending"  # 默认待处理状态
    )
    db.session.add(new_order)
    db.session.commit()

    return {
        "order_id": new_order.order_id,
        "item_id": new_order.item_id,
        "order_quantity": new_order.order_quantity,
        "order_date": new_order.order_date,
        "status": new_order.status
    }, None

def update_inventory_after_order(order_id, status):
    """
    更新补货订单状态，并在状态变为 'completed' 时，增加库存
    """
    order = ReplenishmentOrder.query.get(order_id)
    if not order:
        return None, "订单不存在"

    order.status = status

    # 如果订单完成，增加库存
    if status == "completed":
        inventory = Inventory.query.filter_by(item_id=order.item_id).first()
        if inventory:
            inventory.current_stock += order.order_quantity
        else:
            return None, "库存记录不存在"

    try:
        db.session.commit()
        return {
            "order_id": order.order_id,
            "item_id": order.item_id,
            "order_quantity": order.order_quantity,
            "status": order.status
        }, None
    except Exception as e:
        db.session.rollback()
        return None, f"数据库更新失败: {str(e)}"

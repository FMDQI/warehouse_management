from models.inventory import Inventory
from models.normal_items import NormalItem
from models.sales_records import SalesRecord
from models.sales_predictions import SalesPrediction
from models.replenishment_orders import ReplenishmentOrder
from models.db import db
import datetime
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

def get_all_inventory():
    """
    获取所有库存数据
    """
    inventory = Inventory.query.all()
    return [{
        "inventory_id": item.inventory_id,
        "item_id": item.item_id,
        "current_stock": item.current_stock
    } for item in inventory]

def get_inventory_by_id(inventory_id):
    """
    根据库存 ID 获取单个库存数据
    """
    item = Inventory.query.get(inventory_id)
    if item:
        return {
            "inventory_id": item.inventory_id,
            "item_id": item.item_id,
            "current_stock": item.current_stock
        }
    return None

def create_inventory(item_id, current_stock):
    """
    创建新的库存记录
    """
    new_item = Inventory(item_id=item_id, current_stock=current_stock)
    db.session.add(new_item)
    db.session.commit()
    return {
        "inventory_id": new_item.inventory_id,
        "item_id": new_item.item_id,
        "current_stock": new_item.current_stock
    }

def update_inventory(inventory_id, item_id=None, current_stock=None):
    """
    更新库存记录
    """
    item = Inventory.query.get(inventory_id)
    if not item:
        return None

    if item_id is not None:
        item.item_id = item_id
    if current_stock is not None:
        item.current_stock = current_stock

    db.session.commit()
    return {
        "inventory_id": item.inventory_id,
        "item_id": item.item_id,
        "current_stock": item.current_stock
    }

def delete_inventory(inventory_id):
    """
    删除库存记录
    """
    item = Inventory.query.get(inventory_id)
    if not item:
        return False

    db.session.delete(item)
    db.session.commit()
    return True

def predict_sales_and_generate_orders():
    """
    预测商品销量并自动创建补货订单
    """
    items = NormalItem.query.all()  # 获取所有商品
    today = datetime.date.today()  # 获取今天的日期

    for item in items:
        # 获取该商品的销售记录
        sales_records = SalesRecord.query.filter(SalesRecord.item_id == item.item_id).order_by(SalesRecord.sale_date).all()
        if len(sales_records) < 3:
            continue  # 如果销售记录不足，跳过该商品

        # 准备训练数据
        dates = np.array([(record.sale_date - sales_records[0].sale_date).days for record in sales_records]).reshape(-1, 1)
        sales = np.array([record.sale_quantity for record in sales_records])

        # 训练决策树回归模型
        model = DecisionTreeRegressor()
        model.fit(dates, sales)

        # 预测未来 7 天的销量
        future_dates = np.array([(today - sales_records[0].sale_date).days + i for i in range(1, 8)]).reshape(-1, 1)
        predicted_sales = int(model.predict(future_dates).mean())  # 取 7 天的平均预测销量

        # 获取当前库存
        inventory = Inventory.query.filter(Inventory.item_id == item.item_id).first()
        if not inventory:
            continue  # 如果没有库存记录，跳过该商品

        # 计算预计缺货时间
        estimated_days = inventory.current_stock / max(predicted_sales, 1)

        # 结合保质期计算是否需要补货
        shelf_life_days = item.shelf_life
        production_date = item.production_date
        expiration_date = production_date + datetime.timedelta(days=shelf_life_days)

        # 判断是否需要补货：预计缺货时间小于 7 天且商品未过期
        if estimated_days < 7 and expiration_date > today:
            order_quantity = max(predicted_sales * 2, 10)  # 订购 2 倍的预测销量，最少订购 10 个
            new_order = ReplenishmentOrder(
                item_id=item.item_id,
                order_quantity=order_quantity,
                order_date=today,
                status="pending"
            )
            db.session.add(new_order)

    db.session.commit()


def get_low_stock_items(threshold=10):
    """
    获取库存低于阈值的商品，并进行销量预测以决定是否补货
    """
    low_stock_items = Inventory.query.filter(Inventory.current_stock < threshold).all()
    predicted_orders = []

    for item in low_stock_items:
        predicted_orders.append({
            "inventory_id": item.inventory_id,
            "item_id": item.item_id,
            "current_stock": item.current_stock
        })

    # 进行销量预测并自动补货
    predict_sales_and_generate_orders()

    return predicted_orders

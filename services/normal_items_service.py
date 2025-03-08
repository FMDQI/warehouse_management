from models.normal_items import NormalItem
from models.db import db

def get_all_normal_items():
    """
    获取所有物品数据
    """
    items = NormalItem.query.all()
    return [{
        "item_id": item.item_id,
        "item_name": item.item_name,
        "item_type": item.item_type,
        "production_date": item.production_date.isoformat(),
        "shelf_life": item.shelf_life
    } for item in items]

def get_normal_item_by_id(item_id):
    """
    根据物品 ID 获取单个物品数据
    """
    item = NormalItem.query.get(item_id)
    if item:
        return {
            "item_id": item.item_id,
            "item_name": item.item_name,
            "item_type": item.item_type,
            "production_date": item.production_date.isoformat(),
            "shelf_life": item.shelf_life
        }
    return None

def create_normal_item(item_name, item_type, production_date, shelf_life):
    """
    创建新的物品记录
    """
    new_item = NormalItem(
        item_name=item_name,
        item_type=item_type,
        production_date=production_date,
        shelf_life=shelf_life
    )
    db.session.add(new_item)
    db.session.commit()
    return {
        "item_id": new_item.item_id,
        "item_name": new_item.item_name,
        "item_type": new_item.item_type,
        "production_date": new_item.production_date.isoformat(),
        "shelf_life": new_item.shelf_life
    }

def update_normal_item(item_id, item_name=None, item_type=None, production_date=None, shelf_life=None):
    """
    更新物品记录
    """
    item = NormalItem.query.get(item_id)
    if not item:
        return None

    if item_name is not None:
        item.item_name = item_name
    if item_type is not None:
        item.item_type = item_type
    if production_date is not None:
        item.production_date = production_date
    if shelf_life is not None:
        item.shelf_life = shelf_life

    db.session.commit()
    return {
        "item_id": item.item_id,
        "item_name": item.item_name,
        "item_type": item.item_type,
        "production_date": item.production_date.isoformat(),
        "shelf_life": item.shelf_life
    }

def delete_normal_item(item_id):
    """
    删除物品记录
    """
    item = NormalItem.query.get(item_id)
    if not item:
        return False

    db.session.delete(item)
    db.session.commit()
    return True





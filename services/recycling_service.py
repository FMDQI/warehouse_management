from models.db import db
from models.recyclable_items import RecyclableItem
from models.recycling_records import RecyclingRecord
from sqlalchemy.sql import func

class RecyclingService:
    
    @staticmethod
    def add_recyclable_item(item_name, item_type):
        """添加可回收物品"""
        new_item = RecyclableItem(item_name=item_name, item_type=item_type)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    @staticmethod
    def get_all_recyclable_items():
        """获取所有可回收物品"""
        return RecyclableItem.query.all()

    @staticmethod
    def get_recyclable_item_by_id(item_id):
        """根据ID获取可回收物品"""
        return RecyclableItem.query.get(item_id)

    @staticmethod
    def update_recyclable_item(item_id, new_item_name, new_item_type):
        """更新可回收物品信息"""
        item = RecyclableItem.query.get(item_id)
        if item:
            item.item_name = new_item_name
            item.item_type = new_item_type
            db.session.commit()
            return item
        return None

    @staticmethod
    def delete_recyclable_item(item_id):
        """删除可回收物品"""
        item = RecyclableItem.query.get(item_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_recycling_quantity(item_id):
        """获取某个回收物品的总回收数量"""
        total_quantity = db.session.query(func.sum(RecyclingRecord.quantity))\
            .filter(RecyclingRecord.item_id == item_id)\
            .scalar()
        return {"item_id": item_id, "total_quantity": total_quantity or 0}

    @staticmethod
    def get_all_recycling_quantities():
        """获取所有回收物品的总回收数量"""
        results = db.session.query(
            RecyclingRecord.item_id,
            func.sum(RecyclingRecord.quantity).label('total_quantity')
        ).group_by(RecyclingRecord.item_id).all()

        return [{"item_id": item_id, "total_quantity": total_quantity or 0} for item_id, total_quantity in results]


    @staticmethod
    def add_recycling_record(item_id, quantity, recycle_date):
        """添加回收记录"""
        new_record = RecyclingRecord(item_id=item_id, quantity=quantity, recycle_date=recycle_date)
        db.session.add(new_record)
        db.session.commit()
        return new_record





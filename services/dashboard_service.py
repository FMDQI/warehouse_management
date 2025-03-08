from models.db import db
from models.sales_records import SalesRecord
from models.recycling_records import RecyclingRecord
from models.normal_items import NormalItem
from models.inventory import Inventory
from sqlalchemy.sql import func
from flask import request

class DashboardService:
    @staticmethod
    def get_sales_trend(item_id=None):
        """获取物品的销售数量趋势，可选按 item_id 过滤"""
        query = db.session.query(
            SalesRecord.item_id,
            func.sum(SalesRecord.sale_quantity).label("total_sales"),
            SalesRecord.sale_date
        ).group_by(SalesRecord.item_id, SalesRecord.sale_date)

        if item_id:
            query = query.filter(SalesRecord.item_id == item_id)

        sales_trend = query.all()

        return [{"item_id": item_id, "total_sales": total_sales, "sale_date": str(sale_date)}
                for item_id, total_sales, sale_date in sales_trend]

    @staticmethod
    def get_recycling_trend(item_id=None):
        """获取物品的回收数量趋势，可选按 item_id 过滤"""
        query = db.session.query(
            RecyclingRecord.item_id,
            func.sum(RecyclingRecord.quantity).label("total_recycled"),
            RecyclingRecord.recycle_date
        ).group_by(RecyclingRecord.item_id, RecyclingRecord.recycle_date)

        if item_id:
            query = query.filter(RecyclingRecord.item_id == item_id)

        recycling_trend = query.all()

        return [{"item_id": item_id, "total_recycled": total_recycled, "recycle_date": str(recycle_date)}
                for item_id, total_recycled, recycle_date in recycling_trend]

    @staticmethod
    def get_all_items():
        """获取所有物品信息及库存"""
        items = db.session.query(
            NormalItem.item_id, 
            NormalItem.item_name, 
            NormalItem.item_type,
            NormalItem.production_date, 
            NormalItem.shelf_life,
            Inventory.current_stock
        ).join(Inventory, NormalItem.item_id == Inventory.item_id, isouter=True).all()

        return [{
            "item_id": item[0],
            "item_name": item[1],
            "item_type": item[2],
            "production_date": str(item[3]),
            "shelf_life": item[4],
            "current_stock": item[5] or 0
        } for item in items]

    @staticmethod
    def get_category_sales_trend(item_type=None):
        """获取指定类别的销售趋势"""
        if item_type is None:  # 允许传参，也允许从请求获取
           item_type = request.args.get('item_type')
           
        query = db.session.query(
            NormalItem.item_type,
            func.sum(SalesRecord.sale_quantity).label("total_sales"),
            SalesRecord.sale_date
        ).join(SalesRecord, NormalItem.item_id == SalesRecord.item_id)

        if item_type:
            query = query.filter(NormalItem.item_type == item_type)  # 仅筛选特定类别

        category_sales = query.group_by(NormalItem.item_type, SalesRecord.sale_date).all()

        return [{"item_type": item_type, "total_sales": total_sales, "sale_date": str(sale_date)}
                for item_type, total_sales, sale_date in category_sales]






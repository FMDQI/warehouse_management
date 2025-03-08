from flask import Blueprint, jsonify, request
from services.dashboard_service import DashboardService

bp = Blueprint('dashboard_api', __name__)

@bp.route('/sales_trend', methods=['GET'])
def sales_trend():
    """获取指定物品或所有物品的销售趋势"""
    item_id = request.args.get('item_id', type=int)
    data = DashboardService.get_sales_trend(item_id)
    return jsonify(data)

@bp.route('/recycling_trend', methods=['GET'])
def recycling_trend():
    """获取指定物品或所有物品的回收趋势"""
    item_id = request.args.get('item_id', type=int)
    data = DashboardService.get_recycling_trend(item_id)
    return jsonify(data)

@bp.route('/items', methods=['GET'])
def all_items():
    """获取所有物品信息及库存"""
    data = DashboardService.get_all_items()
    return jsonify(data)

@bp.route('/category_sales_trend', methods=['GET'])
def category_sales_trend():
    """获取指定类别或所有类别的销售趋势"""
    item_type = request.args.get('item_type', type=str)
    data = DashboardService.get_category_sales_trend(item_type)
    return jsonify(data)







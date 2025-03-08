from flask import Blueprint, jsonify, request
from services.orders_service import (
    get_all_orders,
    get_order_by_id,
    create_order,
    update_order,
    delete_order
)

bp = Blueprint('orders_api', __name__)

@bp.route('/orders', methods=['GET'])
def get_all_orders_route():
    """
    获取所有订单数据
    """
    orders = get_all_orders()
    return jsonify(orders), 200

@bp.route('/orders/<int:sale_id>', methods=['GET'])
def get_order_by_id_route(sale_id):
    """
    根据订单 ID 获取单个订单数据
    """
    order = get_order_by_id(sale_id)
    if order:
        return jsonify(order), 200
    return jsonify({"error": "Order not found"}), 404

@bp.route('/orders', methods=['POST'])
def create_order_route():
    """
    创建新的订单记录
    """
    data = request.json
    if not data or 'item_id' not in data or 'sale_quantity' not in data or 'sale_date' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_order = create_order(data['item_id'], data['sale_quantity'], data['sale_date'])
    return jsonify(new_order), 201

@bp.route('/orders/<int:sale_id>', methods=['PUT'])
def update_order_route(sale_id):
    """
    更新订单记录
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    updated_order = update_order(
        sale_id,
        item_id=data.get('item_id'),
        sale_quantity=data.get('sale_quantity'),
        sale_date=data.get('sale_date')
    )
    if updated_order:
        return jsonify(updated_order), 200
    return jsonify({"error": "Order not found"}), 404

@bp.route('/orders/<int:sale_id>', methods=['DELETE'])
def delete_order_route(sale_id):
    """
    删除订单记录
    """
    success = delete_order(sale_id)
    if success:
        return jsonify({"message": "Order deleted"}), 200
    return jsonify({"error": "Order not found"}), 404





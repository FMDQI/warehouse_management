from flask import Blueprint, jsonify, request
from services.replenishment_service import get_low_stock_items, create_replenishment_order, update_inventory_after_order
from models.replenishment_orders import ReplenishmentOrder
from services.inventory_service import predict_sales_and_generate_orders  # 正确导入

bp = Blueprint('replenishment_api', __name__)

@bp.route('/replenishment_orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    """
    更新补货订单状态，并在状态变为 "completed" 时增加库存
    """
    data = request.json
    if 'status' not in data:
        return jsonify({"error": "缺少状态字段"}), 400

    result, error = update_inventory_after_order(order_id, data['status'])
    
    if error:
        return jsonify({"error": error}), 400

    return jsonify(result), 200



@bp.route('/replenishment_orders', methods=['GET'])
def get_replenishment_orders():
    """
    获取所有补货订单
    """
    orders = ReplenishmentOrder.query.all()
    return jsonify([{
        "order_id": order.order_id,
        "item_id": order.item_id,
        "order_quantity": order.order_quantity,
        "order_date": order.order_date,
        "status": order.status
    } for order in orders]), 200

@bp.route('/replenishment_orders', methods=['POST'])
def create_order():
    """
    创建补货订单
    """
    data = request.json
    if not data or 'item_id' not in data or 'order_quantity' not in data:
        return jsonify({"error": "缺少必要字段"}), 400

    result, error = create_replenishment_order(data['item_id'], data['order_quantity'])
    if error:
        return jsonify({"error": error}), 400

    return jsonify(result), 201

@bp.route('/replenishment_orders/low_stock', methods=['GET'])
def get_low_stock_replenishment():
    """
    获取库存低于阈值的商品
    """
    threshold = request.args.get('threshold', default=10, type=int)
    low_stock_items = get_low_stock_items(threshold)
    return jsonify(low_stock_items), 200

@bp.route('/predict_and_order', methods=['POST'])
def predict_and_order():
    try:
        predict_sales_and_generate_orders()  # 调用服务层函数
        return jsonify({"message": "Sales prediction and replenishment orders created successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500








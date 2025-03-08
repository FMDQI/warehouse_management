from flask import Blueprint, jsonify, request
from services.inventory_service import (
    get_all_inventory,
    get_inventory_by_id,
    create_inventory,
    update_inventory,
    delete_inventory
)

bp = Blueprint('inventory_api', __name__)

@bp.route('/', methods=['GET'])
def get_all_inventory_route():
    """
    获取所有库存数据
    """
    inventory = get_all_inventory()
    return jsonify(inventory), 200

@bp.route('/<int:inventory_id>', methods=['GET'])
def get_inventory_by_id_route(inventory_id):
    """
    根据库存 ID 获取单个库存数据
    """
    item = get_inventory_by_id(inventory_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Inventory item not found"}), 404

@bp.route('/', methods=['POST'])
def create_inventory_route():
    """
    创建新的库存记录
    """
    data = request.json
    if not data or 'item_id' not in data or 'current_stock' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_item = create_inventory(data['item_id'], data['current_stock'])
    return jsonify(new_item), 201

@bp.route('/<int:inventory_id>', methods=['PUT'])
def update_inventory_route(inventory_id):
    """
    更新库存记录
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    updated_item = update_inventory(
        inventory_id,
        item_id=data.get('item_id'),
        current_stock=data.get('current_stock')
    )
    if updated_item:
        return jsonify(updated_item), 200
    return jsonify({"error": "Inventory item not found"}), 404

@bp.route('/<int:inventory_id>', methods=['DELETE'])
def delete_inventory_route(inventory_id):
    """
    删除库存记录
    """
    success = delete_inventory(inventory_id)
    if success:
        return jsonify({"message": "Inventory item deleted"}), 200
    return jsonify({"error": "Inventory item not found"}), 404





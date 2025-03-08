from flask import Blueprint, jsonify, request
from services.normal_items_service import (
    get_all_normal_items,
    get_normal_item_by_id,
    create_normal_item,
    update_normal_item,
    delete_normal_item
)

bp = Blueprint('normal_items_api', __name__)

@bp.route('/normal_items', methods=['GET'])
def get_all_normal_items_route():
    """
    获取所有物品数据
    """
    items = get_all_normal_items()
    return jsonify(items), 200

@bp.route('/normal_items/<int:item_id>', methods=['GET'])
def get_normal_item_by_id_route(item_id):
    """
    根据物品 ID 获取单个物品数据
    """
    item = get_normal_item_by_id(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@bp.route('/normal_items', methods=['POST'])
def create_normal_item_route():
    """
    创建新的物品记录
    """
    data = request.json
    if not data or 'item_name' not in data or 'item_type' not in data or 'production_date' not in data or 'shelf_life' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_item = create_normal_item(
        data['item_name'],
        data['item_type'],
        data['production_date'],
        data['shelf_life']
    )
    return jsonify(new_item), 201

@bp.route('/normal_items/<int:item_id>', methods=['PUT'])
def update_normal_item_route(item_id):
    """
    更新物品记录
    """
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    updated_item = update_normal_item(
        item_id,
        item_name=data.get('item_name'),
        item_type=data.get('item_type'),
        production_date=data.get('production_date'),
        shelf_life=data.get('shelf_life')
    )
    if updated_item:
        return jsonify(updated_item), 200
    return jsonify({"error": "Item not found"}), 404

@bp.route('/normal_items/<int:item_id>', methods=['DELETE'])
def delete_normal_item_route(item_id):
    """
    删除物品记录
    """
    success = delete_normal_item(item_id)
    if success:
        return jsonify({"message": "Item deleted"}), 200
    return jsonify({"error": "Item not found"}), 404




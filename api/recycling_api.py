from flask import Blueprint, jsonify, request
from services.recycling_service import RecyclingService

bp = Blueprint('recycling_api', __name__)

@bp.route('/items', methods=['GET'])
def get_all_items():
    """获取所有可回收物品"""
    items = RecyclingService.get_all_recyclable_items()
    return jsonify([{"item_id": item.item_id, "item_name": item.item_name, "item_type": item.item_type} for item in items])

@bp.route('/items/<int:item_id>', methods=['GET'])
def get_item_by_id(item_id):
    """获取指定ID的可回收物品"""
    item = RecyclingService.get_recyclable_item_by_id(item_id)
    if item:
        return jsonify({"item_id": item.item_id, "item_name": item.item_name, "item_type": item.item_type})
    return jsonify({"message": "物品不存在"}), 404

@bp.route('/items', methods=['POST'])
def add_item():
    """添加可回收物品"""
    data = request.json
    item_name = data.get("item_name")
    item_type = data.get("item_type")

    if not item_name or not item_type:
        return jsonify({"message": "物品名称和类型不能为空"}), 400

    new_item = RecyclingService.add_recyclable_item(item_name, item_type)
    return jsonify({"item_id": new_item.item_id, "item_name": new_item.item_name, "item_type": new_item.item_type}), 201

@bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """更新可回收物品信息"""
    data = request.json
    new_item_name = data.get("item_name")
    new_item_type = data.get("item_type")

    if not new_item_name or not new_item_type:
        return jsonify({"message": "物品名称和类型不能为空"}), 400

    updated_item = RecyclingService.update_recyclable_item(item_id, new_item_name, new_item_type)
    if updated_item:
        return jsonify({"item_id": updated_item.item_id, "item_name": updated_item.item_name, "item_type": updated_item.item_type})
    return jsonify({"message": "物品不存在"}), 404

@bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """删除可回收物品"""
    success = RecyclingService.delete_recyclable_item(item_id)
    if success:
        return jsonify({"message": "物品删除成功"})
    return jsonify({"message": "物品不存在"}), 404

@bp.route('/items/quantity', methods=['GET'])
def get_recycling_quantity():
    """获取回收数量"""
    item_id = request.args.get('item_id', type=int)

    if item_id:
        data = RecyclingService.get_recycling_quantity(item_id)
    else:
        data = RecyclingService.get_all_recycling_quantities()

    return jsonify(data)

@bp.route('/records', methods=['POST'])
def add_recycling_record():
    """添加回收记录"""
    data = request.json
    item_id = data.get("item_id")
    quantity = data.get("quantity")
    recycle_date = data.get("recycle_date")

    if not item_id or not quantity or not recycle_date:
        return jsonify({"message": "物品ID、数量和回收日期不能为空"}), 400

    new_record = RecyclingService.add_recycling_record(item_id, quantity, recycle_date)
    return jsonify({"record_id": new_record.record_id, "item_id": new_record.item_id, "quantity": new_record.quantity, "recycle_date": new_record.recycle_date}), 201





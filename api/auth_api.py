from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from services.auth_service import authenticate_user, get_user_by_id

bp = Blueprint('auth_api', __name__)

@bp.route('/login', methods=['POST'])
def login():
    """
    用户登录
    """
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing username or password"}), 400

    # 验证用户
    user = authenticate_user(data['username'], data['password'])
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    # 生成 JWT Token，确保 user_id 是字符串
    access_token = create_access_token(identity=str(user.user_id), additional_claims={"role": user.role})
    return jsonify({
        "access_token": access_token,
        "user_id": user.user_id,
        "role": user.role
        
    }), 200

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    受保护的端点，用于测试 JWT 认证
    """
    current_user_id = str(get_jwt_identity())  # 确保是字符串
    user = get_user_by_id(current_user_id)
    return jsonify({
        "message": "You are logged in!",
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role
    }), 200

@bp.route('/admin', methods=['GET'])
@jwt_required()
def admin_only():
    """
    仅管理员可访问的端点
    """
    current_user_id = str(get_jwt_identity())  # 确保是字符串
    user = get_user_by_id(current_user_id)
    if user.role != 'admin':
        return jsonify({"error": "Admin access required"}), 403

    return jsonify({
        "message": "Welcome, admin!",
        "user_id": user.user_id,
        "username": user.username
    }), 200

@bp.route('/business', methods=['GET'])
@jwt_required()
def business_user_only():
    """
    仅业务用户可访问的端点
    """
    current_user_id = str(get_jwt_identity())  # 确保是字符串
    user = get_user_by_id(current_user_id)
    if user.role != 'business_user':
        return jsonify({"error": "Business user access required"}), 403

    return jsonify({
        "message": "Welcome, business user!",
        "user_id": user.user_id,
        "username": user.username
    }), 200






from werkzeug.security import generate_password_hash, check_password_hash
from models.user_roles import UserRole
from models.db import db

def create_user(username, password, role):
    """
    创建新用户
    """
    # 检查用户名是否已存在
    if UserRole.query.filter_by(username=username).first():
        return None

    # 创建用户
    new_user = UserRole(
        username=username,
        password_hash=generate_password_hash(password),  # 哈希密码
        role=role
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user

def authenticate_user(username, password):
    """
    验证用户登录
    """
    user = UserRole.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

def get_user_by_id(user_id):
    """
    根据用户 ID 获取用户信息
    """
    return UserRole.query.get(user_id)




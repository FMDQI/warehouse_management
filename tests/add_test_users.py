from werkzeug.security import generate_password_hash
from models.db import db
from models.user_roles import UserRole
from app import app

def add_test_users():
    """
    向 user_roles 表中添加测试用户
    """
    with app.app_context():
        # 添加管理员用户
        admin_user = UserRole(
            username='admin',
            password_hash=generate_password_hash('admin123'),  # 哈希密码
            role='admin'
        )
        db.session.add(admin_user)

        # 添加业务用户
        business_user = UserRole(
            username='user',
            password_hash=generate_password_hash('user123'),  # 哈希密码
            role='business_user'
        )
        db.session.add(business_user)

        # 提交事务
        db.session.commit()
        print("成功添加测试用户！")

if __name__ == '__main__':
    add_test_users()





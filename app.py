from flask import Flask
from flask_jwt_extended import JWTManager
from config import SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY
from models.db import db
from api import (
    inventory_api, orders_api, dashboard_api,
    replenishment_api, recycling_api, normal_items_api,
    auth_api  # 新增 auth_api
)
from sqlalchemy import text
from flask_cors import CORS  # 导入 CORS

# 初始化 Flask 应用
app = Flask(__name__)
CORS(app)  # 启用 CORS 支持

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# JWT 配置
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY  # 设置一个安全的密钥
jwt = JWTManager(app)

# 测试数据库连接
with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")

# 注册蓝图
app.register_blueprint(inventory_api.bp, url_prefix='/api/inventory')
app.register_blueprint(orders_api.bp, url_prefix='/api/orders')
app.register_blueprint(dashboard_api.bp, url_prefix='/api/dashboard')
app.register_blueprint(replenishment_api.bp, url_prefix='/api/replenishment')
app.register_blueprint(recycling_api.bp, url_prefix='/api/recycling')
app.register_blueprint(normal_items_api.bp, url_prefix='/api/normal_items')
app.register_blueprint(auth_api.bp, url_prefix='/api/auth')  # 注册 auth_api 蓝图

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

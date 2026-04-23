import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    # 載入環境變數
    load_dotenv()
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__, 
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'))
    
    # 設定 SECRET_KEY
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')
    
    # 初始化資料庫
    from app.models.database import init_db
    init_db()

    # 註冊 Blueprints
    from app.routes.main import main_bp
    from app.routes.record import record_bp
    from app.routes.category import category_bp
    from app.routes.budget import budget_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(record_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(budget_bp)

    return app

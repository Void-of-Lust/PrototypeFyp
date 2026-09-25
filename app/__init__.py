import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    from app.customer.routes import customer_bp
    from app.kitchen.routes import kitchen_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(customer_bp, url_prefix='/')
    app.register_blueprint(kitchen_bp, url_prefix='/kitchen')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

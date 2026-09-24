from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = 'dev-secret-key'

    # Import Blueprints
    from app.customer.routes import customer_bp
    from app.kitchen.routes import kitchen_bp
    from app.admin.routes import admin_bp

    # Register Blueprints with URL prefixes
    app.register_blueprint(customer_bp, url_prefix='/')
    app.register_blueprint(kitchen_bp, url_prefix='/kitchen')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

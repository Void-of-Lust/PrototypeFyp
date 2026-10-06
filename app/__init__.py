import os
from flask import Flask, render_template, request, redirect, url_for, session
from app.extensions import db
from app.models import Admin, Dapur

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'dev-secret-key-123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'database.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            role = request.form.get('role')
            username = request.form.get('username')
            password = request.form.get('password')

            if role == 'admin':
                user = Admin.query.filter_by(nama_admin=username, kata_laluan=password).first()
                if user:
                    session['user_role'] = 'admin'
                    return redirect(url_for('admin.dashboard'))
            elif role == 'dapur':
                user = Dapur.query.filter_by(nama_pengguna=username, kata_laluan=password).first()
                if user:
                    session['user_role'] = 'dapur'
                    return redirect(url_for('kitchen.live_orders'))

            return render_template('login.html', error='Nama pengguna atau kata laluan salah.')

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    from app.customer.routes import customer_bp
    from app.kitchen.routes import kitchen_bp
    from app.admin.routes import admin_bp

    app.register_blueprint(customer_bp)
    app.register_blueprint(kitchen_bp, url_prefix='/kitchen')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

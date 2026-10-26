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

    with app.app_context():
        db.create_all()

        if not Admin.query.filter_by(nama_admin='admin').first():
            db.session.add(Admin(nama_admin='admin', kata_laluan='admin123'))

        if not Dapur.query.filter_by(nama_pengguna='dapur').first():
            db.session.add(Dapur(nama_pengguna='dapur', kata_laluan='dapur123', status=True))

        db.session.commit()

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            role = (request.form.get('role') or '').strip()
            username = (request.form.get('username') or '').strip()
            password = (request.form.get('password') or '').strip()

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

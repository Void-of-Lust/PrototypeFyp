from flask import Blueprint, render_template, request, redirect, url_for, session
from app.extensions import db
from app.models import Menu, Pesanan

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
def restrict_to_admin():
    if session.get('user_role') != 'admin':
        return redirect(url_for('login'))

@admin_bp.route('/dashboard')
def dashboard():
    drinks = Menu.query.all()
    completed_orders = Pesanan.query.filter_by(status_pesanan='Selesai').all()

    # Calculate daily sales totals
    total_sales = sum(order.kuantiti * order.menu.harga for order in completed_orders if order.menu)
    total_orders = len(completed_orders)

    return render_template('admin/dashboard.html', drinks=drinks, total_sales=total_sales, total_orders=total_orders)

@admin_bp.route('/menu/add', methods=['POST'])
def add_menu():
    nama = request.form.get('nama_minuman')
    harga = float(request.form.get('harga', 0.0))

    if nama and harga > 0:
        new_drink = Menu(nama_minuman=nama, harga=harga, status_menu=True)
        db.session.add(new_drink)
        db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/menu/<int:drink_id>/toggle', methods=['POST'])
def toggle_menu(drink_id):
    drink = Menu.query.get_or_404(drink_id)
    drink.status_menu = not drink.status_menu
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/menu/<int:drink_id>/delete', methods=['POST'])
def delete_menu(drink_id):
    drink = Menu.query.get_or_404(drink_id)
    db.session.delete(drink)
    db.session.commit()
    return redirect(url_for('admin.dashboard'))

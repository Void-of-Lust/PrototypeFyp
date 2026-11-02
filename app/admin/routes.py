from flask import Blueprint, render_template, request, redirect, url_for, session
from app.extensions import db
from app.models import Menu, Pesanan, Pelanggan

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
def restrict_to_admin():
    if session.get('user_role') != 'admin':
        return redirect(url_for('login'))

@admin_bp.route('/dashboard')
def dashboard():
    drinks = Menu.query.all()
    completed_orders = Pesanan.query.filter_by(status_pesanan='Selesai').all()

    # Sales metrics
    total_sales = sum(order.kuantiti * order.menu.harga for order in completed_orders if order.menu)
    total_orders = len(completed_orders)
    total_drinks_sold = sum(order.kuantiti for order in completed_orders)

    # Table status grid data (Meja 1 - Meja 6)
    table_list = [f"A{i}" for i in range(1, 7)]
    table_status = {}
    for t in table_list:
        cust = Pelanggan.query.filter_by(no_meja=t).order_by(Pelanggan.id_pelanggan.desc()).first()
        if cust and any(p.status_pesanan != 'Selesai' for p in cust.pesanan):
            table_status[t] = 'ada'
        else:
            table_status[t] = 'tiada'

    # Transaction log history
    transactions = Pesanan.query.order_by(Pesanan.tarikh_masa.desc()).limit(15).all()

    return render_template('admin/dashboardAdmin.html',
                           drinks=drinks,
                           total_sales=total_sales,
                           total_orders=total_orders,
                           total_drinks_sold=total_drinks_sold,
                           table_status=table_status,
                           transactions=transactions)

@admin_bp.route('/menu/add', methods=['POST'])
def add_menu():
    nama = request.form.get('nama_minuman')
    harga = float(request.form.get('harga', 0.0))
    kategori = request.form.get('kategori', 'Panas')

    if nama and harga > 0:
        new_drink = Menu(nama_minuman=nama, harga=harga, kategori=kategori, status_menu=True)
        db.session.add(new_drink)
        db.session.commit()
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/menu/<int:drink_id>/edit', methods=['POST'])
def edit_menu(drink_id):
    drink = Menu.query.get_or_404(drink_id)
    drink.nama_minuman = request.form.get('nama_minuman', drink.nama_minuman)
    drink.harga = float(request.form.get('harga', drink.harga))
    drink.kategori = request.form.get('kategori', drink.kategori)
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

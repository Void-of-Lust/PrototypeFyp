from datetime import datetime, timedelta
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

    # Dynamic 7-Day Sales Calculation from Database
    today = datetime.utcnow().date()
    chart_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    sales_by_date = {d: 0.0 for d in chart_days}

    for order in completed_orders:
        if order.tarikh_masa and order.menu:
            order_date = order.tarikh_masa.date()
            if order_date in sales_by_date:
                sales_by_date[order_date] += float(order.kuantiti * order.menu.harga)

    max_sale = max(sales_by_date.values()) if sales_by_date and max(sales_by_date.values()) > 0 else 1.0
    chart_data = []
    for d in chart_days:
        amount = sales_by_date[d]
        pct = int((amount / max_sale) * 100) if max_sale > 0 else 0
        chart_data.append({
            'date_str': d.strftime('%d/%m'),
            'day_name': d.strftime('%a'),
            'amount': amount,
            'height_pct': max(pct, 6) if amount > 0 else 6
        })

    # Table status grid data (Meja A1 - A6)
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
                           chart_data=chart_data,
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

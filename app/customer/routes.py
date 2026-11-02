import os
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, current_app
from app.extensions import db
from app.models import Menu, Pelanggan, Pesanan

customer_bp = Blueprint('customer', __name__)

# Screen 1: Landing Page & Dining Type Selection
@customer_bp.route('/')
def welcome():
    table_no = request.args.get('table')
    if table_no:
        session['table_number'] = table_no
    current_table = session.get('table_number', 'Dine-In')
    return render_template('customer/welcome.html', table_number=current_table)

@customer_bp.route('/select_type', methods=['POST'])
def select_type():
    jenis = request.form.get('jenis_sajian')
    session['jenis_sajian'] = jenis

    if jenis == 'Minum Sahaja':
        return redirect(url_for('customer.view_menu'))
    return redirect(url_for('customer.upload_food'))

# Screen 2: Food Image / Camera Upload
@customer_bp.route('/upload_food', methods=['GET', 'POST'])
def upload_food():
    if request.method == 'POST':
        file = request.files.get('food_image')
        if file and file.filename != '':
            upload_folder = os.path.join(current_app.static_folder, 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, file.filename)
            file.save(filepath)
            session['food_image'] = file.filename
        return redirect(url_for('customer.view_menu'))
    return render_template('customer/uploadFood.html')

# Screen 3: Drink Menu
@customer_bp.route('/menu')
def view_menu():
    current_table = session.get('table_number', 'Dine-In')
    drinks = Menu.query.filter_by(status_menu=True).all()
    return render_template('customer/menu.html', drinks=drinks, table_number=current_table)

# Screen 4: Submit Order & Save to DB
@customer_bp.route('/order', methods=['POST'])
def place_order():
    table_no = session.get('table_number', 'Dine-In')

    # Create Pelanggan record
    customer = Pelanggan(no_meja=table_no)
    db.session.add(customer)
    db.session.commit()

    drinks = Menu.query.filter_by(status_menu=True).all()
    orders_created = 0

    for drink in drinks:
        qty = int(request.form.get(f'qty_{drink.id_menu}', 0))
        notes = request.form.get(f'notes_{drink.id_menu}', '')

        if qty > 0:
            new_order = Pesanan(
                id_pelanggan=customer.id_pelanggan,
                id_menu=drink.id_menu,
                kuantiti=qty,
                nota_tambahan=notes,
                status_pesanan='Baru'
            )
            db.session.add(new_order)
            orders_created += 1

    if orders_created > 0:
        db.session.commit()
        return redirect(url_for('customer.order_status', customer_id=customer.id_pelanggan))

    return redirect(url_for('customer.view_menu'))

# Screen 5: Live Order Status Page
@customer_bp.route('/status/<int:customer_id>')
def order_status(customer_id):
    customer = Pelanggan.query.get_or_404(customer_id)
    orders = Pesanan.query.filter_by(id_pelanggan=customer_id).all()
    total_price = sum(o.kuantiti * o.menu.harga for o in orders if o.menu)

    return render_template('customer/success.html',
                           table_number=customer.no_meja,
                           orders=orders,
                           total_price=total_price,
                           customer_id=customer_id)

# API Endpoint for Live Polling in success.html
@customer_bp.route('/api/status/<int:customer_id>')
def api_order_status(customer_id):
    orders = Pesanan.query.filter_by(id_pelanggan=customer_id).all()
    data = [{
        'id_pesanan': o.id_pesanan,
        'nama_minuman': o.menu.nama_minuman if o.menu else '',
        'kuantiti': o.kuantiti,
        'status': o.status_pesanan
    } for o in orders]
    return jsonify({'orders': data})

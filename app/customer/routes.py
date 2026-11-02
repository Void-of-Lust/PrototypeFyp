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

    # If "Minum Sahaja", skip camera upload and go directly to menu
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

# Screen 4: Submit Order
@customer_bp.route('/order', methods=['POST'])
def place_order():
    # Retrieve details from session & request form
    table_number = session.get('table_number', 'Dine-In')
    jenis_sajian = session.get('jenis_sajian')
    food_image = session.get('food_image')

    # Redirect to a thank you / confirmation page or clear relevant session items
    return redirect(url_for('customer.welcome'))

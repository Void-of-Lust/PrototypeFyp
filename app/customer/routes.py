from flask import Blueprint, render_template, request, session, redirect, url_for
from app.extensions import db
from app.models import Menu, Pelanggan, Pesanan

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/')
@customer_bp.route('/menu')
def view_menu():
    table_no = request.args.get('table')
    if table_no:
        session['table_number'] = table_no

    current_table = session.get('table_number', 'Dine-In')
    drinks = Menu.query.filter_by(status_menu=True).all()

    return render_template('customer/menu.html', drinks=drinks, table_number=current_table)

@customer_bp.route('/order', methods=['POST'])
def place_order():
    table_no = request.form.get('table_number', 'Dine-In')

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
        return render_template('customer/success.html', table_number=table_no)

    return redirect(url_for('customer.view_menu'))

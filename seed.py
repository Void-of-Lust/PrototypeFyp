from flask import Blueprint, render_template, request, session, redirect, url_for
from app.extensions import db
from app.models import Menu, Pelanggan, Pesanan

customer_bp = Blueprint('customer', __name__)


@customer_bp.route('/')
@customer_bp.route('/menu')
def view_menu():
    table_no = (request.args.get('table') or '').strip()

    if table_no:
        session['table_number'] = table_no
    elif 'table_number' not in session:
        session['table_number'] = 'Dine-In'

    current_table = session.get('table_number', 'Dine-In')
    drinks = Menu.query.filter_by(status_menu=True).all()

    return render_template('customer/menu.html', drinks=drinks, table_number=current_table)


@customer_bp.route('/order', methods=['POST'])
def place_order():
    table_no = (request.form.get('table_number') or '').strip() or 'Dine-In'
    session['table_number'] = table_no

    drinks = Menu.query.filter_by(status_menu=True).all()
    valid_items = []

    for drink in drinks:
        raw_qty = (request.form.get(f'qty_{drink.id_menu}', '') or '').strip()
        if raw_qty == '':
            continue

        try:
            qty = int(raw_qty)
        except (TypeError, ValueError):
            continue

        if qty <= 0:
            continue

        notes = (request.form.get(f'notes_{drink.id_menu}', '') or '').strip()
        valid_items.append((drink, qty, notes))

    if not valid_items:
        return redirect(url_for('customer.view_menu', table=table_no))

    customer = Pelanggan(no_meja=table_no)
    db.session.add(customer)
    db.session.commit()

    for drink, qty, notes in valid_items:
        db.session.add(Pesanan(
            id_pelanggan=customer.id_pelanggan,
            id_menu=drink.id_menu,
            kuantiti=qty,
            nota_tambahan=notes,
            status_pesanan='Baru'
        ))

    db.session.commit()
    return render_template('customer/success.html', table_number=table_no)

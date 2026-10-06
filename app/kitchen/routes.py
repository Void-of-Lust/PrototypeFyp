from flask import Blueprint, render_template, request, redirect, url_for, session
from app.extensions import db
from app.models import Pesanan

kitchen_bp = Blueprint('kitchen', __name__)

@kitchen_bp.before_request
def restrict_to_kitchen():
    if session.get('user_role') not in ['dapur', 'admin']:
        return redirect(url_for('login'))

@kitchen_bp.route('/orders')
def live_orders():
    # Active orders only (excluding 'Selesai') sorted by newest first
    orders = Pesanan.query.filter(Pesanan.status_pesanan != 'Selesai').order_by(Pesanan.tarikh_masa.desc()).all()
    return render_template('kitchen/dashboard.html', orders=orders)

@kitchen_bp.route('/order/<int:order_id>/status', methods=['POST'])
def update_status(order_id):
    order = Pesanan.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status:
        order.status_pesanan = new_status
        db.session.commit()
    return redirect(url_for('kitchen.live_orders'))

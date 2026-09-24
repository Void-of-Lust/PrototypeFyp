from flask import Blueprint

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/')
def home():
    return "Customer Page: Welcome to the Drink Ordering App!"
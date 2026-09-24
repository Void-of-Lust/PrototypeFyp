from flask import Blueprint

kitchen_bp = Blueprint('kitchen', __name__)

@kitchen_bp.route('/')
def kitchen_dashboard():
    return "Kitchen Page: Incoming Drink Orders"

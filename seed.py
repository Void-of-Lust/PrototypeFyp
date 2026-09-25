from app import create_app
from app.extensions import db
from app.models import Admin, Dapur, Menu
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Insert default Admin if none exists
    if not Admin.query.first():
        admin_user = Admin(
            nama_admin='admin',
            kata_laluan=generate_password_hash('admin123')
        )
        db.session.add(admin_user)

    # Insert default Kitchen staff if none exists
    if not Dapur.query.first():
        kitchen_user = Dapur(
            nama_pengguna='dapur1',
            kata_laluan=generate_password_hash('dapur123'),
            status=True
        )
        db.session.add(kitchen_user)

    # Insert initial Beverage Menu items if table is empty
    if not Menu.query.first():
        sample_drinks = [
            Menu(nama_minuman='Teh Tarik', harga=2.50, status_menu=True),
            Menu(nama_minuman='Kopi O Panas', harga=2.00, status_menu=True),
            Menu(nama_minuman='Milo Ais', harga=3.50, status_menu=True),
            Menu(nama_minuman='Sirap Bandung', harga=3.00, status_menu=True),
            Menu(nama_minuman='Jus Epal', harga=4.50, status_menu=False) # Out of stock sample
        ]
        db.session.add_all(sample_drinks)

    db.session.commit()
    print("Database seeding completed successfully!")

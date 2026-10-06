from app import create_app
from app.extensions import db
from app.models import Admin, Dapur, Menu

app = create_app()

with app.app_context():
    db.create_all()

    # Create default Admin if not exists
    if not Admin.query.filter_by(nama_admin="admin").first():
        admin_user = Admin(nama_admin="admin", kata_laluan="admin123")
        db.session.add(admin_user)

    # Create default Kitchen user if not exists
    if not Dapur.query.filter_by(nama_pengguna="dapur").first():
        kitchen_user = Dapur(nama_pengguna="dapur", kata_laluan="dapur123", status=True)
        db.session.add(kitchen_user)

    # Seed sample drinks catalog
    if Menu.query.count() == 0:
        sample_drinks = [
            Menu(nama_minuman="Teh Tarik", harga=3.00, status_menu=True),
            Menu(nama_minuman="Kopi O Peng", harga=3.50, status_menu=True),
            Menu(nama_minuman="Milo Ais", harga=4.00, status_menu=True),
            Menu(nama_minuman="Jus Epal", harga=5.00, status_menu=True),
            Menu(nama_minuman="Sirap Bandung", harga=3.20, status_menu=False),
        ]
        db.session.add_all(sample_drinks)

    db.session.commit()
    print("Database successfully seeded with initial admin, kitchen staff, and menu items.")

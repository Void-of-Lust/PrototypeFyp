from app import create_app
from app.extensions import db
from app.models import Admin, Dapur, Menu

app = create_app()

with app.app_context():
    db.create_all()

    if not Admin.query.filter_by(nama_admin="admin").first():
        db.session.add(Admin(nama_admin="admin", kata_laluan="admin123"))

    if not Dapur.query.filter_by(nama_pengguna="dapur").first():
        db.session.add(Dapur(nama_pengguna="dapur", kata_laluan="dapur123", status=True))

    if Menu.query.count() == 0:
        sample_drinks = [
            Menu(nama_minuman="Teh Tarik", harga=3.00, kategori="Panas", status_menu=True),
            Menu(nama_minuman="Kopi O Peng", harga=3.50, kategori="Sejuk", status_menu=True),
            Menu(nama_minuman="Milo Ais", harga=4.00, kategori="Sejuk", status_menu=True),
            Menu(nama_minuman="Jus Epal", harga=5.00, kategori="Sejuk", status_menu=True),
            Menu(nama_minuman="Sirap Bandung", harga=3.20, kategori="Sejuk", status_menu=False),
        ]
        db.session.add_all(sample_drinks)

    db.session.commit()
    print("Database updated and seeded with drink categories.")

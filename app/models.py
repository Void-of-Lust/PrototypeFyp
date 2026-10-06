from datetime import datetime
from app.extensions import db

class Admin(db.Model):
    __tablename__ = 'admin'
    id_admin = db.Column(db.Integer, primary_key=True)
    nama_admin = db.Column(db.String(50), nullable=False)
    kata_laluan = db.Column(db.String(255), nullable=False)

class Dapur(db.Model):
    __tablename__ = 'dapur'
    id_dapur = db.Column(db.Integer, primary_key=True)
    nama_pengguna = db.Column(db.String(50), nullable=False)
    kata_laluan = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, default=True)

class Pelanggan(db.Model):
    __tablename__ = 'pelanggan'
    id_pelanggan = db.Column(db.Integer, primary_key=True)
    no_meja = db.Column(db.String(20), nullable=False)
    pesanan = db.relationship('Pesanan', backref='pelanggan', lazy=True)

class Menu(db.Model):
    __tablename__ = 'menu'
    id_menu = db.Column(db.Integer, primary_key=True)
    nama_minuman = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Numeric(10, 2), nullable=False)
    status_menu = db.Column(db.Boolean, default=True) # True = Ada, False = Habis
    pesanan = db.relationship('Pesanan', backref='menu', lazy=True)

class Pesanan(db.Model):
    __tablename__ = 'pesanan'
    id_pesanan = db.Column(db.Integer, primary_key=True)
    id_pelanggan = db.Column(db.Integer, db.ForeignKey('pelanggan.id_pelanggan'), nullable=False)
    id_menu = db.Column(db.Integer, db.ForeignKey('menu.id_menu'), nullable=False)
    tarikh_masa = db.Column(db.DateTime, default=datetime.utcnow)
    status_pesanan = db.Column(db.String(20), default='Baru') # 'Baru', 'Diproses', 'Selesai'
    nota_tambahan = db.Column(db.String(255), nullable=True)
    kuantiti = db.Column(db.Integer, default=1, nullable=False)

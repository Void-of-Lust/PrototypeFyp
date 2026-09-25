from datetime import datetime
from app.extensions import db

class Admin(db.Model):
    __tablename__ = 'ADMIN'

    id_admin = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_admin = db.Column(db.String(50), nullable=False)
    kata_laluan = db.Column(db.String(255), nullable=False)

class Dapur(db.Model):
    __tablename__ = 'DAPUR'

    id_dapur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_pengguna = db.Column(db.String(50), nullable=False)
    kata_laluan = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, default=True, nullable=False)

    pesanan_handled = db.relationship('Pesanan', backref='dapur', lazy=True)

class Menu(db.Model):
    __tablename__ = 'MENU'

    id_menu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_minuman = db.Column(db.String(100), nullable=False)
    harga = db.Column(db.Numeric(10, 2), nullable=False)
    status_menu = db.Column(db.Boolean, default=True, nullable=False)

    pesanan = db.relationship('Pesanan', backref='menu', lazy=True)

class Pelanggan(db.Model):
    __tablename__ = 'PELANGGAN'

    id_pelanggan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    no_meja = db.Column(db.String(20), nullable=False)

    pesanan = db.relationship('Pesanan', backref='pelanggan', lazy=True)

class Pesanan(db.Model):
    __tablename__ = 'PESANAN'

    id_pesanan = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pelanggan = db.Column(db.Integer, db.ForeignKey('PELANGGAN.id_pelanggan', ondelete='CASCADE'), nullable=False)
    id_menu = db.Column(db.Integer, db.ForeignKey('MENU.id_menu', ondelete='CASCADE'), nullable=False)
    id_dapur = db.Column(db.Integer, db.ForeignKey('DAPUR.id_dapur', ondelete='SET NULL'), nullable=True)
    
    tarikh_masa = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status_pesanan = db.Column(db.Enum('Baru', 'Diproses', 'Selesai'), default='Baru', nullable=False)
    kuantiti = db.Column(db.Integer, default=1, nullable=False)
    nota_tambahan = db.Column(db.String(255), nullable=True)

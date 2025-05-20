from factory import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    status = db.Column(db.String(20), nullable=False, default='pending')
    # Tambah kolom untuk data verifikasi
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    jurusan = db.Column(db.String(50))
    bukti_pembayaran = db.Column(db.String(200))
    ijasah = db.Column(db.String(200))
    foto_diri = db.Column(db.String(200))
    # Tambah kolom untuk pembayaran
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid/pending/paid
    payment_proof = db.Column(db.String(200))
    bank_name = db.Column(db.String(50))
    sender_name = db.Column(db.String(100))

    @property
    def is_profile_complete(self):
        required_fields = ['full_name', 'address', 'phone', 'birth_date', 'class_level']
        return all(getattr(self, field, None) for field in required_fields)

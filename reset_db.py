from factory import create_app, db
from models import User

app = create_app()

with app.app_context():
    # Hapus semua tabel
    db.drop_all()
    
    # Buat ulang tabel
    db.create_all()
    
    # Buat admin baru
    admin = User(username="admin", password="admin123", role="admin", status="accepted")
    db.session.add(admin)
    db.session.commit()
    
print("Database berhasil direset!")

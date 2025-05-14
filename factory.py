from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret-key'  # tambahkan secret key untuk flash
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        from models import User  # ...existing code...
        db.create_all()  # Membuat tabel jika belum ada

    @app.route('/')
    def home():
        # Menggunakan template base.html untuk menampilkan halaman utama.
        return render_template("base.html")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            # ...existing code untuk proses login, misalnya validasi...
            return redirect(url_for('student_verification'))
        return render_template("login.html")

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            return redirect(url_for('login'))
        return render_template("register.html")

    @app.route('/student_verification', methods=['GET', 'POST'])
    def student_verification():
        from flask import request, redirect, url_for, flash
        if request.method == 'POST':
            # ...tambahkan logika untuk memproses verifikasi...
            flash("Verifikasi berhasil diajukan.")
            return redirect(url_for('home'))
        return render_template("student_verification.html")

    @app.route('/admin_dashboard')
    def admin_dashboard():
        from models import User
        users = User.query.all()
        return render_template("admin_dashboard.html", users=users)

    @app.route('/admin/accept/<int:user_id>', methods=['POST'])
    def admin_accept(user_id):
        from models import User
        user = User.query.get(user_id)
        if user:
            user.status = "accepted"
            db.session.commit()
            flash(f"User {user.username} telah diterima.")
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/reject/<int:user_id>', methods=['POST'])
    def admin_reject(user_id):
        from models import User
        user = User.query.get(user_id)
        if user:
            user.status = "rejected"
            db.session.commit()
            flash(f"User {user.username} telah ditolak.")
        return redirect(url_for('admin_dashboard'))

    @app.route('/admin/detail/<int:user_id>', methods=['GET'])
    def admin_detail(user_id):
        from models import User
        user = User.query.get(user_id)
        if user:
            return render_template("admin_detail.html", user=user)
        return redirect(url_for('admin_dashboard'))

    @app.route('/pendaftaran', methods=['GET', 'POST'])
    def pendaftaran():
        from flask import request, redirect, url_for, flash
        if request.method == 'POST':
            # ...tambahkan logika untuk memproses data pendaftaran...
            flash("Pendaftaran berhasil.")
            return redirect(url_for('home'))
        return render_template("pendaftaran.html")

    @app.errorhandler(404)
    def not_found(error):
        return ("The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.", 404)

    return app

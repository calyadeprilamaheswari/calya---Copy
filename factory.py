from flask import Flask, render_template, request, redirect, url_for, flash, session  # Add session here
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from werkzeug.utils import secure_filename

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret-key'  # tambahkan secret key untuk flash
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    with app.app_context():
        from models import User
        db.create_all()
        # Pastikan anda menghapus file "user.db" lama
        if not User.query.filter_by(username="admin").first():
            admin = User(username="admin", password="admin123", role="admin", status="accepted")
            db.session.add(admin)
            db.session.commit()

    @app.route('/')
    def home():
        return render_template("base.html")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        from models import User
        if request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username, password=password).first()
            if user:
                if user.role == "admin":
                    flash("Gunakan halaman admin login untuk admin")
                    return redirect(url_for("admin_login"))
                session["user_id"] = user.id  # Now session is defined
                
                # Jika belum mengisi form pendaftaran
                if not user.full_name:
                    return redirect(url_for('student_verification'))
                else:
                    return redirect(url_for('student_dashboard'))
                    
            flash("Username atau password salah")
            return redirect(url_for("login"))
        return render_template("login.html")
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        from models import User
        if request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")
            if User.query.filter_by(username=username).first():
                flash("Username sudah digunakan")
                return redirect(url_for("register"))
            new_user = User(username=username, password=password, role="user", status="pending")
            db.session.add(new_user)
            db.session.commit()
            flash("Pendaftaran berhasil, silahkan login")
            return redirect(url_for("login"))
        return render_template("register.html")

    # Tambahkan route admin_login untuk admin
    @app.route('/admin_login', methods=['GET', 'POST'])
    def admin_login():
        from models import User
        from flask import session
        if request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username, password=password, role="admin").first()
            if user:
                session["user_id"] = user.id
                return redirect(url_for("admin_dashboard"))
            else:
                flash("Invalid admin credentials")
                return redirect(url_for("admin_login"))
        return render_template("admin_login.html")
        
    @app.route('/student_verification', methods=['GET', 'POST'])
    def student_verification():
        if request.method == 'POST':
            user_id = session.get("user_id")
            if user_id:
                user = User.query.get(user_id)
                if user:
                    try:
                        # Simpan data form ke database
                        user.full_name = request.form.get('full_name')
                        user.phone = request.form.get('phone')
                        user.address = request.form.get('address')
                        user.jurusan = request.form.get('jurusan')
                        user.status = "pending"
                        db.session.commit()
                        flash("Pendaftaran berhasil! Silakan tunggu beberapa hari untuk verifikasi dari admin.", "success")
                        return redirect(url_for('home'))  # Redirect ke home setelah verifikasi

                    except Exception as e:
                        flash(f"Error: {str(e)}", "error")
                        return redirect(url_for('home'))

            flash("Anda harus login terlebih dahulu")
            return redirect(url_for('login'))
            
        return render_template("student_verification.html")
        
    # Tambahkan route student_dashboard untuk siswa
    @app.route('/student_dashboard')
    def student_dashboard():
        from models import User
        from flask import session
        user_id = session.get("user_id")
        if user_id:
            user = User.query.get(user_id)
            if user:
                return render_template("student_dashboard.html", user=user)
        flash("Anda harus login terlebih dahulu.")
        return redirect(url_for('login'))
        
    @app.route('/admin_dashboard')
    def admin_dashboard():
        from models import User
        users = User.query.filter(User.role != 'admin').all()
        return render_template("admin_dashboard.html", users=users, 
                             total_pendaftar=len(users),
                             total_diterima=len([u for u in users if u.status == 'accepted']),
                             total_ditolak=len([u for u in users if u.status == 'rejected']),
                             total_pending=len([u for u in users if u.status == 'pending']))

    # Fix admin_report route
    @app.route('/admin/report')
    def admin_report():
        from models import User
        
        # Get basic statistics
        users = User.query.filter(User.role != 'admin').all()
        siswa_diterima = User.query.filter_by(status='accepted').all()  # Add this line
        total_sudah_bayar = User.query.filter_by(payment_status='paid').count()
        total_belum_bayar = User.query.filter_by(status='accepted').filter(
            (User.payment_status != 'paid') | (User.payment_status == None)
        ).count()

        # Get jurusan stats
        jurusan_stats = []
        for jurusan in ['IPA', 'IPS', 'Bahasa', 'Teknik']:
            total = User.query.filter_by(jurusan=jurusan).count()
            diterima = User.query.filter_by(jurusan=jurusan, status='accepted').count()
            jurusan_stats.append({
                'nama': jurusan,
                'total': total,
                'diterima': diterima
            })

        return render_template('admin_report.html',
            total_pendaftar=len(users),
            total_diterima=len([u for u in users if u.status == 'accepted']),
            total_ditolak=len([u for u in users if u.status == 'rejected']),
            total_pending=len([u for u in users if u.status == 'pending']),
            siswa_diterima=siswa_diterima,  # Add this line
            jurusan_stats=jurusan_stats,
            total_sudah_bayar=total_sudah_bayar,
            total_belum_bayar=total_belum_bayar,
            total_pembayaran=total_sudah_bayar * 500000
        )

    @app.route('/admin/accept/<int:user_id>', methods=['POST'])
    def admin_accept(user_id):
        from models import User
        user = User.query.get(user_id)
        if user:
            user.status = "accepted"
            db.session.commit()
            flash(f"User {user.username} telah diterima dan dapat melakukan pembayaran.")
            # Send to payment page automatically
            return redirect(url_for('payment', user_id=user.id))
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

    @app.route('/admin/delete/<int:user_id>', methods=['POST'])
    def admin_delete(user_id):
        from models import User
        user = User.query.get(user_id)
        if user and user.role != 'admin':  # Prevent admin deletion
            try:
                # Delete from database
                db.session.delete(user)
                db.session.commit()
                flash(f"User {user.username} telah dihapus.", "success")
            except Exception as e:
                flash(f"Error menghapus user: {str(e)}", "error")
                
        return redirect(url_for('admin_dashboard'))

    @app.route('/logout')
    def logout():
        session.clear()  # Clear all session data
        flash('Anda telah berhasil logout', 'success')
        return redirect(url_for('home'))  # Redirect to home page

    @app.errorhandler(404)
    def not_found(error):
        return ("The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.", 404)

    @app.route('/payment', methods=['GET', 'POST'])
    def payment():
        user_id = session.get("user_id")
        if not user_id:
            flash("Anda harus login terlebih dahulu", "error")
            return redirect(url_for("login"))
            
        user = User.query.get(user_id)
        if user and user.status == "accepted":
            return render_template("payment.html", user=user)
        else:
            flash("Anda belum diterima atau tidak memiliki akses ke halaman ini", "error")
            return redirect(url_for("student_dashboard"))

    @app.route('/submit_payment', methods=['POST'])
    def submit_payment():
        user_id = session.get("user_id")
        if not user_id:
            flash("Anda harus login terlebih dahulu", "error")
            return redirect(url_for("login"))
            
        user = User.query.get(user_id)
        if user and user.status == "accepted":
            try:
                file = request.files['payment_proof']
                if file.filename:
                    filename = f"payment_{user.id}_{secure_filename(file.filename)}"
                    file.save(os.path.join('static', 'uploads', filename))
                    user.payment_proof = filename
                    user.payment_status = "pending"
                    user.bank_name = request.form.get('bank_name')
                    user.sender_name = request.form.get('sender_name')
                    db.session.commit()
                    flash("Bukti pembayaran berhasil diupload", "success")
                    return redirect(url_for("student_dashboard"))
            except Exception as e:
                flash(f"Error: {str(e)}", "error")
                
        return redirect(url_for("student_dashboard"))

    return app

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

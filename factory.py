from flask import Flask, render_template, request, redirect, url_for, flash, session  # Add session here
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.utils import secure_filename  # Add this import
import os  # Add this import for file operations

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
                session["user_id"] = user.id
                
                # Cek apakah user sudah pernah mendaftar
                if not user.full_name:
                    # Belum pernah mendaftar, arahkan ke form pendaftaran
                    return redirect(url_for("student_verification"))
                else:
                    # Sudah pernah mendaftar, arahkan ke dashboard untuk cek status
                    flash("Anda sudah melakukan pendaftaran. Silakan cek status pendaftaran Anda.")
                    return redirect(url_for("student_dashboard"))
                
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
        from models import User
        if request.method == 'POST':
            user_id = session.get("user_id")
            if user_id:
                user = User.query.get(user_id)
                if user:
                    # Simpan data form ke database
                    user.full_name = request.form.get('full_name')
                    user.gender = request.form.get('gender')  # Add this line
                    user.phone = request.form.get('phone')
                    user.address = request.form.get('address')
                    user.jurusan = request.form.get('jurusan')
                    user.tempat_lahir = request.form.get('tempat_lahir')  # Tambah ini
                    user.asal_sekolah = request.form.get('asal_sekolah')  # Tambah ini
                    user.nama_ayah = request.form.get('nama_ayah')  # Tambah ini
                    user.nama_ibu = request.form.get('nama_ibu')    # Tambah ini
                    user.status = "pending"

                    # Handle file uploads if present
                    if 'ijasah' in request.files:
                        file = request.files['ijasah']
                        if file and file.filename:
                            filename = f"ijasah_{user.id}_{secure_filename(file.filename)}"
                            file.save(os.path.join('static', 'uploads', filename))
                            user.ijasah = filename

                    if 'foto_diri' in request.files:
                        file = request.files['foto_diri']
                        if file and file.filename:
                            filename = f"foto_{user.id}_{secure_filename(file.filename)}"
                            file.save(os.path.join('static', 'uploads', filename))
                            user.foto_diri = filename

                    db.session.commit()
                    flash("Verifikasi Anda telah dikirim, silakan cek status di dashboard Anda.")
                    return redirect(url_for('student_dashboard'))
            else:
                flash("Anda harus login terlebih dahulu untuk mengajukan verifikasi.")
                return redirect(url_for('login'))
        return render_template("student_verification.html")
        
    # Tambahkan route student_dashboard untuk siswa
    @app.route('/student_dashboard')
    def student_dashboard():
        from models import User
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
        # Tampilkan data siswa (non-admin) saja sehingga hanya data verifikasi yang diisi muncul
        users = User.query.filter(User.role != 'admin').all()
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

    @app.route('/admin/report')
    def admin_report():
        from models import User
        
        # Get basic statistics
        users = User.query.filter(User.role != 'admin').all()
        siswa_diterima = User.query.filter_by(status='accepted').all()
        total_sudah_bayar = User.query.filter_by(payment_status='paid').count()
        total_belum_bayar = User.query.filter_by(status='accepted').filter(
            (User.payment_status != 'paid') | (User.payment_status == None)
        ).count()

        # Get jurusan stats
        jurusan_stats = []
        for jurusan in ['IPA', 'IPS']:  # Remove 'Bahasa' and 'Teknik'
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
            siswa_diterima=siswa_diterima,
            jurusan_stats=jurusan_stats,
            total_sudah_bayar=total_sudah_bayar,
            total_belum_bayar=total_belum_bayar,
            total_pembayaran=total_sudah_bayar * 500000
        )

    @app.route('/informasi-sekolah')
    def informasi_sekolah():
        from models import Schedule
        schedules = Schedule.query.all()
        return render_template('informasi_sekolah.html', schedules=schedules)

    @app.errorhandler(404)
    def not_found(error):
        return ("The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.", 404)

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
        # Clear session
        session.clear()
        flash('Berhasil logout')
        return redirect(url_for('home'))

    @app.route('/payment', methods=['GET', 'POST'])
    def payment():
        from models import User
        user_id = session.get("user_id")
        if not user_id:
            flash("Anda harus login terlebih dahulu", "error")
            return redirect(url_for("login"))
            
        user = User.query.get(user_id)
        if user and user.status == "accepted" and user.payment_status == 'unpaid':
            return render_template("payment.html", user=user)
        else:
            flash("Anda sudah melakukan pembayaran atau belum diterima", "error")
            return redirect(url_for("student_dashboard"))

    @app.route('/submit_payment', methods=['POST'])
    def submit_payment():
        from models import User
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

    @app.route('/admin/verify_payment/<int:user_id>', methods=['POST'])
    def verify_payment(user_id):
        from models import User
        user = User.query.get(user_id)
        if user:
            user.payment_status = 'paid'
            db.session.commit()
            flash(f"Pembayaran untuk {user.username} telah diverifikasi", "success")
        return redirect(url_for('admin_detail', user_id=user.id))

    @app.route('/admin/schedules')
    def admin_schedules():
        from models import Schedule
        schedules = Schedule.query.all()
        return render_template('admin_schedules.html', schedules=schedules)

    @app.route('/admin/schedule/add', methods=['POST'])
    def add_schedule():
        from models import Schedule
        if request.method == 'POST':
            new_schedule = Schedule(
                jurusan=request.form.get('jurusan'),
                waktu=request.form.get('waktu'),
                senin=request.form.get('senin'),
                selasa=request.form.get('selasa'),
                rabu=request.form.get('rabu'),
                kamis=request.form.get('kamis'),
                jumat=request.form.get('jumat')
            )
            db.session.add(new_schedule)
            db.session.commit()
            flash('Jadwal berhasil ditambahkan', 'success')
        return redirect(url_for('admin_schedules'))

    @app.route('/admin/schedule/delete/<int:id>', methods=['POST'])
    def delete_schedule(id):
        from models import Schedule
        schedule = Schedule.query.get_or_404(id)
        db.session.delete(schedule)
        db.session.commit()
        flash('Jadwal berhasil dihapus', 'success')
        return redirect(url_for('admin_schedules'))

    @app.route('/admin/schedule/edit/<int:id>', methods=['POST'])
    def edit_schedule(id):
        from models import Schedule
        schedule = Schedule.query.get_or_404(id)
        if request.method == 'POST':
            schedule.waktu = request.form.get('waktu')
            schedule.senin = request.form.get('senin')
            schedule.selasa = request.form.get('selasa')
            schedule.rabu = request.form.get('rabu')
            schedule.kamis = request.form.get('kamis')
            schedule.jumat = request.form.get('jumat')
            db.session.commit()
            flash('Jadwal berhasil diupdate', 'success')
        return redirect(url_for('admin_schedules'))

    return app

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

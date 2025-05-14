from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        from models import User 
        db.create_all() 

    @app.route('/')
    def home():
        return render_template("base.html")

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            return redirect(url_for('student_verification'))
        return render_template("login.html")

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            return redirect(url_for('login'))
        return render_template("register.html")

    @app.route('/student_verification', methods=['GET'])
    def student_verification():
        return render_template("student_verification.html")

    @app.errorhandler(404)
    def not_found(error):
        return ("The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.", 404)

    return app

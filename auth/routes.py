from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user, login_required
from flask_mail import Message

auth = Blueprint('auth', __name__)

@auth.route('/verify-email')
@login_required
def verify_email():
    if current_user.is_verified:
        return redirect(url_for('main.index'))
    return render_template('verify_email.html')

@auth.route('/send-verification')
@login_required
def send_verification():
    # Add your email sending logic here
    flash('Verification email has been sent!', 'success')
    return redirect(url_for('auth.verify_email'))

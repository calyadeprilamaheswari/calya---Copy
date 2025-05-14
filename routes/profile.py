from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from models import db, User

profile = Blueprint('profile', __name__)

@profile.route('/complete-profile', methods=['GET', 'POST'])
@login_required
def complete_profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.address = request.form.get('address')
        current_user.phone = request.form.get('phone')
        current_user.birth_date = request.form.get('birth_date')
        current_user.class_level = request.form.get('class_level')
        
        db.session.commit()
        flash('Profile completed successfully!', 'success')
        return redirect(url_for('main.index'))
        
    return render_template('profile/complete_profile.html')

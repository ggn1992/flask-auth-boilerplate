from flask import (
    flash, g, redirect, render_template, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.user.models import User, db
from app.auth.forms import ResetPasswordRequestForm, LoginRequestForm, RegisterUserRequestForm, PasswordChangeRequestForm
from app.auth.utils import login_required
from app.email import send_email
import logging

logger = logging.getLogger(__name__)

from app.auth import bp

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        error = None
        user = User.query.filter_by(email=email).first()
        if user is None:
            error = 'Incorrect email.'
        elif user.is_active is False:
            error = 'Account is not active.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))

        flash(error, 'warning')

    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("main.index"))

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterUserRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        error = None

        try:
            user = User(email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            logger.info(f"New user registered: {email}")
            send_email('Welcome to Our App', [email], '<p>Thank you for registering!</p>')
        except Exception as e:
            error = f"User {email} is already registered."
            logger.error(f"Error registering user {email}: {e}")
        else:
            flash('Your registration was successful. Please check your emails to activate your account.', 'success')
            return redirect(url_for("auth.login"))

        if error:
            flash(error, 'warning')

    return render_template('auth/register.html', form=form)

@bp.route('/change-password', methods=('GET', 'POST'))
@login_required
def change_password():
    form = PasswordChangeRequestForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        repeat_password = form.repeat_password.data
        user = g.user
        error = None

        if not check_password_hash(user.password, current_password):
            error = 'Incorrect current password.'
        elif new_password != repeat_password:
            error = 'New passwords do not match.'
        else:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            logger.info(f"Password changed for user: {user.email}")
            flash('Your password has been updated.', 'success')
            return redirect(url_for('main.index'))

        if error:
            flash(error, 'warning')

    return render_template('auth/change-password.html', form=form)

@bp.route('/forgot-password', methods=('GET', 'POST'))
def forgot_password():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        error = None
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'Incorrect email.'
        else:
            reset_token = "dummy-token"
            reset_link = url_for('auth.reset_password', token=reset_token, _external=True)
            send_email(current_app, 'Password Reset Request', [email], f'<p>Click <a href="{reset_link}">here</a> to reset your password.</p>')
            logger.info(f"Password reset requested for {email}")
            flash('Password reset link has been sent to your email.', 'success')

        if error:
            flash(error)

    return render_template('auth/forgot-password.html', form=form)

from flask import (
    flash, g, redirect, render_template, session, url_for
)
import uuid
from werkzeug.security import check_password_hash, generate_password_hash
from app.user.models import User, ActivationCode, PasswordResetCode, db
from app.auth.forms import ResetPasswordRequestForm, LoginRequestForm, RegisterUserRequestForm, PasswordChangeRequestForm, SetNewPasswordForm
from app.auth.utils import login_required, password_check
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

        # Check password complexity
        password_validity = password_check(password)
        if not password_validity['password_ok']:
            error = 'Password does not meet complexity requirements:'
            if password_validity['length_error']:
                error += ' must be at least 8 characters long.'
            if password_validity['digit_error']:
                error += ' must contain at least one digit.'
            if password_validity['uppercase_error']:
                error += ' must contain at least one uppercase letter.'
            if password_validity['lowercase_error']:
                error += ' must contain at least one lowercase letter.'
            if password_validity['symbol_error']:
                error += ' must contain at least one symbol.'

        if not error:
            try:
                user = User(email=email, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()

                activation_code = ActivationCode(user_id=user.id, code=str(uuid.uuid4()))
                db.session.add(activation_code)
                db.session.commit()
                logger.info(f"New user registered: {email}")

                activation_link = url_for('auth.activate_account', code=activation_code.code, _external=True)
                email_body = f"""
                <p>Thank you for registering!</p>
                <p>To activate your account, click <a href="{activation_link}">this</a> link.</p>
                """
                send_email('Welcome to our App', [email], email_body)

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
            # Check password complexity
            password_validity = password_check(new_password)
            if not password_validity['password_ok']:
                error = 'Password does not meet complexity requirements:'
                if password_validity['length_error']:
                    error += ' must be at least 8 characters long.'
                if password_validity['digit_error']:
                    error += ' must contain at least one digit.'
                if password_validity['uppercase_error']:
                    error += ' must contain at least one uppercase letter.'
                if password_validity['lowercase_error']:
                    error += ' must contain at least one lowercase letter.'
                if password_validity['symbol_error']:
                    error += ' must contain at least one symbol.'
            
            if not error:
                user.password = generate_password_hash(new_password)
                db.session.commit()
                logger.info(f"Password changed for user: {user.email}")
                flash('Your password has been updated.', 'success')
                return redirect(url_for('main.index'))

        if error:
            flash(error, 'warning')

    return render_template('auth/change-password.html', form=form)

@bp.route('/activate_account/<code>')
def activate_account(code):
    activation_code = ActivationCode.query.filter_by(code=code, is_active=True).first()
    if activation_code:
        user = User.query.get(activation_code.user_id)
        if user:
            user.is_active = True
            activation_code.is_active = False
            db.session.commit()
            flash('Your account has been activated! You can now log in.', 'success')
            logger.info(f"User {user.email} activated their account.")
            return redirect(url_for('auth.login'))
        else:
            flash('User associated with this activation code not found.', 'warning')
            logger.error(f"Activation failed: User not found for activation code {code}")
    else:
        flash('Invalid or expired activation code.', 'warning')
        logger.error(f"Activation failed: Invalid or expired activation code {code}")

    return redirect(url_for('main.index'))

@bp.route('/reset_password', methods=('GET', 'POST'))
def reset_password():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        error = None
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'Incorrect email.'
        else:
            password_reset_code = PasswordResetCode(user_id=user.id, code=str(uuid.uuid4()))
            db.session.add(password_reset_code)
            db.session.commit()
            reset_link = url_for('auth.reset_password_code', code=password_reset_code.code, _external=True)
            email_body = f'<p>Click <a href="{reset_link}">here</a> to reset your password.</p>'
            send_email('Password Reset Request', [email], email_body)
            logger.info(f"Password reset requested for {email}")
            flash('Password reset link has been sent to your email.', 'success')

        if error:
            flash(error, 'warning')

    return render_template('auth/reset-password.html', form=form)

@bp.route('/reset_password/<code>', methods=('GET', 'POST'))
def reset_password_code(code):
    form = SetNewPasswordForm()
    if form.validate_on_submit():
        password_reset_code = PasswordResetCode.query.filter_by(code=code, is_active=True).first()
        if password_reset_code:
            user = User.query.get(password_reset_code.user_id)
            if user:
                new_password = form.new_password.data
                # Check password complexity
                password_validity = password_check(new_password)
                if not password_validity['password_ok']:
                    error = 'Password does not meet complexity requirements:'
                    if password_validity['length_error']:
                        error += ' must be at least 8 characters long.'
                    if password_validity['digit_error']:
                        error += ' must contain at least one digit.'
                    if password_validity['uppercase_error']:
                        error += ' must contain at least one uppercase letter.'
                    if password_validity['lowercase_error']:
                        error += ' must contain at least one lowercase letter.'
                    if password_validity['symbol_error']:
                        error += ' must contain at least one symbol.'
                    flash(error, 'warning')
                else:
                    user.password = generate_password_hash(new_password)
                    password_reset_code.is_active = False
                    db.session.commit()
                    flash('Your password has been reset. You can now log in with your new password.', 'success')
                    logger.info(f"Password reset for user: {user.email}")
                    return redirect(url_for('auth.login'))
            else:
                flash('User associated with this reset code not found.', 'warning')
                logger.error(f"Password reset failed: User not found for reset code {code}")
        else:
            flash('Invalid or expired password reset code.', 'warning')
            logger.error(f"Password reset failed: Invalid or expired reset code {code}")

    return render_template('auth/set-new-password.html', form=form)

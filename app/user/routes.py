from flask import (
    flash, g, redirect, render_template, session, url_for, current_app
)
from app.user.models import Profile, db
from app.user.forms import UserProfileForm
from app.auth.utils import login_required
import logging

logger = logging.getLogger(__name__)

from app.user import bp

@bp.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
    user = g.user
    profile = Profile.query.filter_by(user_id=user.id).first()

    form = UserProfileForm(obj=profile)

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data

        if profile is None:
            profile = Profile(user_id=user.id, first_name=first_name, last_name=last_name)
            db.session.add(profile)
        else:
            profile.first_name = first_name
            profile.last_name = last_name

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('main.index'))

    return render_template('user/profile.html', form=form)
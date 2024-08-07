from flask import Blueprint, g, session
from app.user.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

from app.auth import routes

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
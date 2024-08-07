from flask import render_template
from app.auth.utils import login_required

from app.main import bp

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('main/index.html')

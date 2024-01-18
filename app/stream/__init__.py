import functools

from flask import Blueprint, render_template, request

bp = Blueprint('stream', __name__, url_prefix='/stream')


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        # create a new stream
        pass
    return render_template('stream/create.html')


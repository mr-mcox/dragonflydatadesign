from flask import current_app
from . import main


@main.route('/pr_data')
def get_pr_data():
    return current_app.send_static_file('pr_data.json')

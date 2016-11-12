from flask import current_app, render_template
from . import main


@main.route('/pr_data')
def get_pr_data():
    return current_app.send_static_file('pr_data.json')

@main.route('/project_robin')
def project_robin():
    return render_template('project_robin.html')

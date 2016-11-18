from flask import current_app, render_template, url_for
from . import main
from . import portfolio_content


@main.route('/pr_data')
def get_pr_data():
    return current_app.send_static_file('pr_data.json')


@main.route('/project_robin')
def project_robin():
    return render_template('project_robin.html')


@main.route('/portfolio/<p_id>')
def portfolio_page(p_id):
    return render_template('portfolio_1.html')


@main.route('/portfolio/<p_id>/page/<page>')
def portfolio_details(p_id, page):
    content = portfolio_content.get_page_content(portfolio_item=p_id, page=page)

    next_url = None
    if not portfolio_content.is_last_page(p_id, page):
        next_url = url_for('main.portfolio_details', p_id=p_id, page=int(page)+1)

    prev_url = None
    if not portfolio_content.is_first_page(p_id, page):
        prev_url = url_for('main.portfolio_details', p_id=p_id, page=int(page)-1)

    return render_template('portfolio_detail.html', content=content, next_url=next_url, prev_url=prev_url)

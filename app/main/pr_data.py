from flask import current_app, render_template, url_for, g
from . import main
# from . import portfolio_content
from .portfolio import Portfolio
import yaml
import os

APP_ROOT = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
APP_STATIC = os.path.join(APP_ROOT, 'static')

with open(os.path.join(APP_STATIC, 'portfolio_content.yml')) as yml_file:
    portfolio_data = yaml.load(yml_file)


def set_portfolio_content():
    g.portfolio_content = Portfolio(data=portfolio_data)


@main.before_request
def attach_content():
    set_portfolio_content()


@main.route('/pr_data')
def get_pr_data():
    return current_app.send_static_file('pr_data.json')


@main.route('/project_robin')
def project_robin():
    return render_template('project_robin.html')


@main.route('/portfolio/<p_id>')
def portfolio_page(p_id):
    return render_template('portfolio_{}.html'.format(p_id))


@main.route('/portfolio/<p_id>/page/<page>')
def portfolio_details(p_id, page):
    content = g.portfolio_content.get_page_content(
        portfolio_item=p_id, page=page)

    next_url = None
    if not g.portfolio_content.is_last_page(p_id, page):
        next_url = url_for(
            'main.portfolio_details', p_id=p_id, page=int(page)+1)

    prev_url = None
    if not g.portfolio_content.is_first_page(p_id, page):
        prev_url = url_for(
            'main.portfolio_details', p_id=p_id, page=int(page)-1)

    portfolio_main = url_for('main.portfolio_page', p_id=p_id)

    links = {
        'next_url': next_url,
        'prev_url': prev_url,
        'portfolio_main': portfolio_main,
    }

    return render_template('portfolio_detail.html', content=content, links=links)

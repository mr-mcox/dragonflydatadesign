from flask import current_app, render_template, url_for, g
from . import main
# from . import portfolio_content
from .portfolio import Portfolio

portfolio_data = [
    [{'title': 'The Situation', 'picture': 'pr-1-spreadsheet.png',
      'copy': 'We learned from a regional data analyst that a challenge that coaches in his region faced was in sharing the long term development arc of teachers with other staff who supported them. Coaches had difficulty reconstructing what occurred weeks and months prior as their only analysis tools were spreadsheets that tabulated current results.'},
     {'title': 'The Next Page', 'picture': 'pr-2-exploration.png',
      'copy': 'To address this need, we applied lean design principles to pilot an interactive high level view on teacher data.'}]
]


def set_portfolio_content():
    g.portfolio_content = Portfolio(data=portfolio_data)
    print('Setting live content')


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
    return render_template('portfolio_1.html')


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

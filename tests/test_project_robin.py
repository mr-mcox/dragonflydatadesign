import json
from flask import url_for


def test_get_data(client, app):
    resp = client.get(url_for('main.get_pr_data'))
    data = json.loads(resp.data.decode('utf-8'))
    assert type(data['cms']) is list


def test_get_portfolio_page(client, app):
    resp = client.get(url_for('main.portfolio_page', id=1))
    assert b'Project Robin' in resp.data

import json
from flask import url_for
from unittest.mock import patch


def test_get_data(client, app):
    resp = client.get(url_for('main.get_pr_data'))
    data = json.loads(resp.data.decode('utf-8'))
    assert type(data['cms']) is list


def test_get_portfolio_page(client, app):
    resp = client.get(url_for('main.portfolio_page', id=1))
    assert b'Project Robin' in resp.data

# Generate page from mocked get page content


def test_page_from_content(client, app):
    with patch('app.main.portfolio.Portfolio.get_page_content') as mock_get_content:
        rv = {'title': 'The title', 'copy':'Some text'}
        mock_get_content.return_value = rv
        resp = client.get(url_for('main.portfolio_details', id=1, page=1))
        assert b'The title' in resp.data
        assert b'Some text' in resp.data

# Return content from passed page and portfolio item

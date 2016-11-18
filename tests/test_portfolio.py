import json
from flask import url_for
from unittest.mock import patch
from app.main.portfolio import Portfolio


def test_get_data(client, app):
    resp = client.get(url_for('main.get_pr_data'))
    data = json.loads(resp.data.decode('utf-8'))
    assert type(data['cms']) is list


def test_get_portfolio_page(client, app):
    resp = client.get(url_for('main.portfolio_page', id=1))
    assert b'Project Robin' in resp.data


def test_page_from_content(client, app):
    with patch('app.main.portfolio.Portfolio.get_page_content') as mock_get_content:
        rv = {'title': 'The title', 'copy': 'Some text', 'picture': 'img.png'}
        mock_get_content.return_value = rv
        resp = client.get(url_for('main.portfolio_details', id=1, page=1))
        assert b'The title' in resp.data
        assert b'Some text' in resp.data
        assert bytes(
            url_for('static', filename=rv['picture']), 'utf-8') in resp.data


def test_get_page_content():
    p_in = [
        [{'title': 'Some title', 'copy': 'Some text', 'picture': 'img.png'}],
        [
            {'title': 'The title', 'copy': 'Some text', 'picture': 'img.png'},
            {'title': 'The title 2', 'copy': 'Some text',
                'picture': 'img.png'},
        ]
    ]
    p = Portfolio(p_in)
    assert p.get_page_content(portfolio_item=1, page=1) == p_in[0][0]
    assert p.get_page_content(portfolio_item=2, page=1) == p_in[1][0]
    assert p.get_page_content(portfolio_item=2, page=2) == p_in[1][1]

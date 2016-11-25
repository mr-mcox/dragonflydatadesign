import json
from flask import url_for, g
from unittest.mock import patch, PropertyMock
from app.main.portfolio import Portfolio
import pytest
import app

@pytest.fixture(autouse=True)
def set_empty_portfolio_content(monkeypatch):
    print('Setting mocked portfolio content')
    def mock_set_content():
        data = [[{}, {}], [{}, {}]]
        g.portfolio_content = Portfolio(data=data)
    monkeypatch.setattr(app.main.pr_data, 'set_portfolio_content', mock_set_content)


def test_get_data(client, app):
    resp = client.get(url_for('main.get_pr_data'))
    data = json.loads(resp.data.decode('utf-8'))
    assert type(data['cms']) is list


def test_get_portfolio_page(client, app):
    resp = client.get(url_for('main.portfolio_page', p_id=1))
    assert b'Project Robin' in resp.data


def test_page_from_content(client, app):
    with patch('app.main.portfolio.Portfolio.get_page_content') as mock_get_content:
        rv = {'title': 'The title', 'copy': 'Some text', 'picture': 'img.png'}
        mock_get_content.return_value = rv
        resp = client.get(url_for('main.portfolio_details', p_id=1, page=1))
        assert b'The title' in resp.data
        assert b'Some text' in resp.data
        assert bytes(
            url_for('static', filename=rv['picture']), 'utf-8') in resp.data


@pytest.fixture
def portfolio_content():
    p_in = [
        [{'title': 'Some title', 'copy': 'Some text', 'picture': 'img.png'}],
        [
            {'title': 'The title', 'copy': 'Some text', 'picture': 'img.png'},
            {'title': 'The title 2', 'copy': 'Some text',
                'picture': 'img.png'},
        ]
    ]
    return p_in


def test_get_page_content(portfolio_content):
    p = Portfolio(portfolio_content)
    assert p.get_page_content(
        portfolio_item=1, page=1) == portfolio_content[0][0]
    assert p.get_page_content(
        portfolio_item=2, page=1) == portfolio_content[1][0]
    assert p.get_page_content(
        portfolio_item=2, page=2) == portfolio_content[1][1]


def test_is_last_page(portfolio_content):
    p = Portfolio(portfolio_content)
    assert p.is_last_page(1, 1) == True
    assert p.is_last_page(2, 1) == False


def test_is_first_page(portfolio_content):
    p = Portfolio(portfolio_content)
    assert p.is_first_page(1, 1) == True
    assert p.is_first_page(2, 2) == False


def test_portfolio_page_has_next_if_not_last(client, app):
    with patch('app.main.portfolio.Portfolio.is_last_page') as mock:
        mock.return_value = False
        resp = client.get(url_for('main.portfolio_details', p_id=1, page=1))
        assert bytes(
            url_for('main.portfolio_details', p_id=1, page=2), 'utf-8') in resp.data


def test_portfolio_page_no_next_if_last(client, app):
    with patch('app.main.portfolio.Portfolio.is_last_page') as mock:
        mock.return_value = True
        resp = client.get(url_for('main.portfolio_details', p_id=1, page=1))
        assert bytes(
            url_for('main.portfolio_details', p_id=1, page=2), 'utf-8') not in resp.data
        assert b'Next Page' not in resp.data


def test_portfolio_page_has_prev_if_not_first(client, app):
    with patch('app.main.portfolio.Portfolio.is_first_page') as mock:
        mock.return_value = False
        resp = client.get(
            url_for('main.portfolio_details', p_id=2, page=2))
        assert bytes(
            url_for('main.portfolio_details', p_id=2, page=1), 'utf-8') in resp.data


def test_portfolio_page_no_prev_if_first(client, app):
    with patch('app.main.portfolio.Portfolio.is_first_page') as mock:
        mock.return_value = True
        resp = client.get(url_for('main.portfolio_details', p_id=1, page=1))
        assert bytes(
            url_for('main.portfolio_details', p_id=1, page=0), 'utf-8') not in resp.data
        assert b'Previous Page' not in resp.data

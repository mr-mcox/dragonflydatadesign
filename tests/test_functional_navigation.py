import pytest
from selenium import webdriver
from flask import url_for


@pytest.mark.usefixtures('live_server')
class TestLiveServer:

    @pytest.fixture(scope='class')
    def browser(self, request):
        browser = webdriver.Firefox()

        def quit_browser():
            browser.quit()

        request.addfinalizer(quit_browser)
        return browser

    # @pytest.mark.xfail

    @pytest.mark.usefixtures('live_server')
    def test_navigate_to_projects(self, browser, app):
        # When user navigates to main page
        browser.get(url_for('main.index', _external=True))
        # Then they get a page
        assert 'Dragonfly Data' in browser.title

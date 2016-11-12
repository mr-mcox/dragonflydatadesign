import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import url_for


@pytest.mark.selenium
@pytest.mark.usefixtures('live_server')
class TestLiveServer:

    @pytest.fixture(scope='class')
    def browser(self, request):
        browser = webdriver.Firefox()

        def quit_browser():
            browser.quit()

        request.addfinalizer(quit_browser)
        return browser

    @pytest.mark.current
    @pytest.mark.usefixtures('live_server')
    def test_navigate_to_projects(self, browser, app):
        # When user navigates to main page
        browser.get(url_for('main.index', _external=True))
        # Then they get a page
        assert 'Dragonfly Data' in browser.title
        # When they click on portfolio button 1
        browser.find_element_by_id('portfolio_1').click()
        # They are taken to a page about project robin
        try:
            WebDriverWait(browser, 5).until(
                EC.title_contains('Project Robin')
            )
        except:
            assert False, "Couldn't find Project Robin in title"

    @pytest.mark.usefixtures('live_server')
    def test_project_robin_has_elements(self, browser, app):
        browser.get(url_for('main.project_robin', _external=True))
        assert browser.find_element_by_class_name('legend') is not None

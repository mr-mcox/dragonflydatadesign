import pytest
from selenium import webdriver
from flask import url_for


@pytest.fixture(scope='class')
def browser(request):
    browser = webdriver.Firefox()

    def quit_browser():
        browser.quit()

    request.addfinalizer(quit_browser)
    return browser


def test_selenium():
    driver = webdriver.Firefox()
    driver.get("http://www.python.org")
    assert "Python" in driver.title

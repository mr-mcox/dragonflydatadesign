import pytest
from app import create_app

@pytest.fixture(scope='session')
def app():
    print('Creating App!!')
    app = create_app()
    return app

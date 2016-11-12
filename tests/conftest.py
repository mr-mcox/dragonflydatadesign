import pytest
import sys
print(sys.path)
from app import create_app


@pytest.fixture(scope='session')
def app():
    app = create_app()
    return app

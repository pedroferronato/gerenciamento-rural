from app import application
import pytest


@pytest.fixture
def client():
    application.config['TESTING'] = True

    with application.test_client() as client:
        yield client

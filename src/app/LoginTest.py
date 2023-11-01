import pytest
from flask.testing import FlaskClient
from app import app


@pytest.fixture
def client() -> FlaskClient:
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_successful_login(client):
    response = client.post('/home',
                           data={'email': 'komuna.dimuna@gmail.com', 'password': 'Password123', 'submit': 'Login'})
    assert response.status_code == 200


def test_failed_login(client):
    response = client.post('/home',
                           data={'email': 'komuna.dimuna@gmail.com', 'password': 'invalidpassword', 'submit': 'Login'})
    assert b'Login failed' in response.data

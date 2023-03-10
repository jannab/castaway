import pytest

import app


@pytest.fixture
def client():
    client = app.app.test_client()
    yield client


def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'

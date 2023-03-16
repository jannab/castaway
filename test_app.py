import pytest

from app import create_app
from models import setup_db

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    database_path = 'postgresql://postgres@127.0.0.1:5432/castaway_test'
    setup_db(app, database_path=database_path)

    yield app


@pytest.fixture
def client():
    client = app.test_client()
    yield client


def test_get_actors(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'

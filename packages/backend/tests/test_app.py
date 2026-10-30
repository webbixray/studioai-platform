import pytest
import json

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello(client):
    rv = client.get('/')
    assert rv.status_code == 200
    data = json.loads(rv.get_data(as_text=True))
    assert data['message'] == 'Hello from StudioAI backend'

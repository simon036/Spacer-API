import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register(client):
    response = client.post('/api/auth/register', json={
        "email": "test@example.com",
        "password": "password123",
        "role": "client"
    })
    assert response.status_code == 201
    assert b"Registration successful" in response.data
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

def test_create_space(client):
    # Simulate login and get JWT token (mock or use a fixture)
    token = "your_jwt_token_here"
    response = client.post(
        '/api/spaces/',
        json={
            "name": "Test Room",
            "description": "A test room for events.",
            "price_per_hour": 50.0
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test Room"
    assert data["price_per_hour"] == 50.0
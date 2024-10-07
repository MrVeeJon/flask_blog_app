import pytest
import os
import sys

# Ensure the app module is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from models import User

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"  # In-memory database for testing
    })
    
    with app.app_context():
        db.create_all()  # Create tables

        # Pre-populate some data for tests
        user = User(username="testuser")
        user.set_password("testpassword")
        db.session.add(user)
        db.session.commit()

        yield app

        db.drop_all()  # Clean up after tests

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def runner(app):
    return app.test_cli_runner()



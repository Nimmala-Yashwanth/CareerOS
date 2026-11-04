import os
import tempfile
from pathlib import Path

# Set database before importing application modules.
_tmpdir = tempfile.TemporaryDirectory()
os.environ['DATABASE_URL'] = 'sqlite:///' + str(Path(_tmpdir.name) / 'test.db')
os.environ['SECRET_KEY'] = 'test-secret-not-for-production'

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c

@pytest.fixture()
def auth(client):
    response = client.post('/api/auth/register', json={'email':'alice@example.com','password':'long-password-123'})
    assert response.status_code == 201, response.text
    return {'Authorization': 'Bearer ' + response.json()['access_token']}

from fastapi.testclient import TestClient
import importlib, os


def test_health_and_version():
    os.environ.setdefault('DATABASE_URL', 'sqlite:///./test_ci.sqlite3')
    os.environ.setdefault('JWT_SECRET', 'ci-secret')
    app = importlib.import_module('app.main').app
    # ensure DB exists
    from app import db
    db.init_db()
    client = TestClient(app)
    r = client.get('/v1/health')
    assert r.status_code == 200
    assert 'status' in r.json()
    r2 = client.get('/v1/version')
    assert r2.status_code == 200

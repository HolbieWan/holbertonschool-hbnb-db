import sys
import os
import pytest

# Ajouter dynamiquement le répertoire src au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from solutions.solution.src import create_app, db
from solutions.solution.src.models.user import User
from solutions.solution.src.persistence.db import DBRepository

@pytest.fixture(scope='module')
def test_app():
    app = create_app(config_class="src.config.TestingConfig")
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def init_db(test_app):
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

def test_save_and_get_user(test_app, init_db):
    repo = DBRepository()
    user = User(id="1", email='test@example.com', password='password')
    repo.save(user)
    retrieved_user = repo.get('user', user.id)
    assert retrieved_user is not None
    assert retrieved_user.email == 'test@example.com'

def test_get_all_users(test_app, init_db):
    repo = DBRepository()
    user1 = User(id="2", email='test1@example.com', password='password1')
    user2 = User(id="3", email='test2@example.com', password='password2')
    repo.save(user1)
    repo.save(user2)
    users = repo.get_all('user')
    assert len(users) == 2

def test_update_user(test_app, init_db):
    repo = DBRepository()
    user = repo.get('user', '1')
    assert user is not None
    user.email = 'updated@example.com'
    repo.update(user)
    updated_user = repo.get('user', '1')
    assert updated_user.email == 'updated@example.com'

def test_delete_user(test_app, init_db):
    repo = DBRepository()
    user = repo.get('user', '1')
    assert user is not None
    repo.delete(user)
    deleted_user = repo.get('user', '1')
    assert deleted_user is None

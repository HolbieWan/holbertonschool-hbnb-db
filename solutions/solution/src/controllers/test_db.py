from flask import Flask
from config import config
from flask_migrate import Migrate
from app import db
from app import app

@app.route('/test_db')
def test_db():
    try:
        # Try to create a new user (or any other model)
        user = User(email="test@example.com", first_name="Test", last_name="User", password="password")
        db.session.add(user)
        db.session.commit()

        # Fetch the user back from the database
        user_from_db = User.query.filter_by(email="test@example.com").first()
        return f"User {user_from_db.first_name} {user_from_db.last_name} created successfully!", 200
    except Exception as e:
        return str(e), 500

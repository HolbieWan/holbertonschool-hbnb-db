from flask.cli import FlaskGroup
from app import app  # Import the app from app.py
from solutions.solution.src.persistence.dbinit import db
from flask_migrate import Migrate

migrate = Migrate(app, db)
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()

import os
from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from src.models.base import db
from app import create_app

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    os.environ['FLASK_ENV'] = 'development'
    os.environ['STORAGE_TYPE'] = 'db'
    manager.run()

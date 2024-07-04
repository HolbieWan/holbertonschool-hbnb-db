import os

class Config:
    STORAGE_TYPE = os.getenv('STORAGE_TYPE', 'db')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://admin:admin@5432/production_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
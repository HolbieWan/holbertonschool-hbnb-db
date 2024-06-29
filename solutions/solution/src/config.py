import os

basedir = os.path.abspath(os.path.dirname(__file__))
print(f"Base directory is set to: {basedir}")

class Config:
    STORAGE_TYPE = os.getenv('STORAGE_TYPE', 'db')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'development.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print(f"Development database URI is set to: {SQLALCHEMY_DATABASE_URI}")

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'database.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print(f"Production database URI is set to: {SQLALCHEMY_DATABASE_URI}")

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

import os


class Config(object):
    """Base configuration."""
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """Production configuration."""
    db_username = os.getenv('DBUSER')
    db_password = os.getenv('DBPWD')
    db_host = os.getenv('DBHOST')
    db_name = os.getenv('DBNAME')
    database_path = database_path = "postgresql://{}:{}@{}/{}".format(
        db_username,
        db_password,
        db_host,
        db_username
    )

    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = database_path


class DevConfig(Config):
    """Development configuration."""
    ENV = 'development'
    DEBUG = True
    DB_NAME = 'dev_car.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.APP_DIR, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)


class TestConfig(Config):
    """Test configuration."""
    DB_NAME = 'test_car.db'
    TESTING = True
    DEBUG = True
    # Put the db file in project root
    DB_PATH = os.path.join(Config.APP_DIR, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)

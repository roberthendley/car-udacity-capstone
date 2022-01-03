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
        db_name
    )

    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = database_path


class DevConfig(Config):
    """Development configuration."""
    ENV = 'development'
    DEBUG = True
    db_username = os.getenv('DEV_DBUSER')
    db_password = os.getenv('DEV_DBPWD')
    db_host = os.getenv('DEV_DBHOST')
    db_name = os.getenv('DEV_DBNAME')
    database_path = database_path = "postgresql://{}:{}@{}/{}".format(
        db_username,
        db_password,
        db_host,
        db_name
    )
    SQLALCHEMY_DATABASE_URI = database_path

class TestConfig(Config):
    """Test configuration."""
    ENV = 'testing'
    TESTING = True
    DEBUG = True

    db_username = os.getenv('TEST_DBUSER')
    db_password = os.getenv('TEST_DBPWD')
    db_host = os.getenv('TEST_DBHOST')
    db_name = os.getenv('TEST_DBNAME')
    database_path = database_path = "postgresql://{}:{}@{}/{}".format(
        db_username,
        db_password,
        db_host,
        db_name
    )
    SQLALCHEMY_DATABASE_URI = database_path

# services/users/project/config.py

import os


class BaseConfig:
    """Base conf"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0
    DEFAULT_MAIL_SENDER = os.getenv('DEFAULT_MAIL_SENDER')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
    MAIL_DEBUG = False
    MAIL_SUPPRESS_SEND = True


class DevelopmentConfig(BaseConfig):
    """Development conf"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG_TB_ENABLED = True
    BCRYPT_LOG_ROUNDS = 4
    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = False


class TestingConfig(BaseConfig):
    """Testing conf"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3


class ProductionConfig(BaseConfig):
    """Production conf"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = False

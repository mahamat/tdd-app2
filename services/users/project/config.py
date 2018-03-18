# services/users/project/config.py

import os

class BaseConfig:
  """Base conf"""
  TESTING = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECRET_KEY = 'my_precious'

class DevelopmentConfig(BaseConfig):
  """Development conf"""
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(BaseConfig):
  """Testing conf"""
  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')

class ProductionConfig(BaseConfig):
  """Production conf"""
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
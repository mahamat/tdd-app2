# services/users/manage.py

from flask.cli import FlaskGroup
from project import create_app, db
import unittest
from project.api.models import User
import coverage

COV = coverage.coverage(
  branch = True,
  include = 'project/*',
  omit = [
    'project/tests/*',
    'project/config.py'
  ]
)

COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def recreate_db():
  db.drop_all()
  db.create_all()
  db.session.commit()

@cli.command()
def seed_db():
  """Seeds the database."""
  db.session.add(User(username='mahamat1', email="mahamat1@example.com", password="greaterthaneight"))
  db.session.add(User(username='mahamat2', email="mahamat2@example.com", password="greaterthaneight"))
  db.session.commit()

@cli.command()
def test():
  """ Runs the tests without code coverage"""
  tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
  result = unittest.TextTestRunner(verbosity=2).run(tests)
  if result.wasSuccessful():
    return 0
  return 1

@cli.command()
def cov():
  """Runs the unit test coverage"""
  tests = unittest.TestLoader().discover('project/tests')
  result = unittest.TextTestRunner(verbosity=2).run(tests)
  if result.wasSuccessful():
    COV.stop()
    COV.save()
    print('Coverage summary')
    COV.report()
    COV.html_report()
    COV.erase()
    return 0
  return 1

if __name__ == '__main__':
  cli()
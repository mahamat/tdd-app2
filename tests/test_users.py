# services/users/project/tests/test_users.py

import json
import unittest
from project import db
from project.api.models import User

from project.tests.base import BaseTestCase


# helper function to add users 
def add_user(username, email):
  user = User(username=username, email=email)
  db.session.add(user)
  db.session.commit()
  return user

class TestUsersService(BaseTestCase):
  """Tests for the users service. """

  def tests_user(self):
    """Ensure the /ping route behaves correctly"""
    response = self.client.get('/users/ping')
    data = json.loads(response.data.decode())
    self.assertEqual(response.status_code, 200)
    self.assertIn('pong', data['message'])
    self.assertIn('success', data['status'])

  def test_add_user(self):
    """Ensure that new user can be added to database"""
    with self.client:
      response = self.client.post(
        '/users',
        data = json.dumps({
          'username':'mahamat',
          'email':'mahamat@example.com'
        }),
        content_type = 'application/json'
      )
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 201)
      self.assertIn('mahamat@example.com was added!', data['message'])
      self.assertIn('success', data['status'])

  def test_add_user_invalid_json(self):
    """Ensure error is thrown if the JSON object is empty."""
    with self.client:
      response = self.client.post(
        '/users',
        data=json.dumps({}),
        content_type='application/json',
      )
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 400)
      self.assertIn('Invalid payload', data['message'])
      self.assertIn('fail', data['status'])

  def test_add_user_invalid_json_keys(self):
    """Ensure error is thrown if the JSON object does not have a username key."""
    with self.client:
      response = self.client.post(
        '/users',
        data=json.dumps({'email': 'mahamat@example.com'}),
        content_type='application/json',
      )
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 400)
      self.assertIn('Invalid payload', data['message'])
      self.assertIn('fail', data['status'])
  
  def test_add_user_duplicate_email(self):
    """Ensure error is thrown if the email already exists."""
    with self.client:
      self.client.post(
        '/users',
        data = json.dumps({
          'username':'mahamat',
          'email':'mahamat@example.com'
        }),
        content_type = 'application/json'
      )
      response = self.client.post(
        '/users',
        data = json.dumps({
          'username':'mahamat',
          'email':'mahamat@example.com'
        }),
        content_type = 'application/json'
      )
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 400)
      self.assertIn('Sorry. That email already exists.', data['message'])
      self.assertIn('fail', data['status'])

  def test_single_user(self):
    """Ensure get single user behaves correctly."""
    user = add_user('mahamat', 'mahamat@example.com')
    with self.client:
      response = self.client.get(f'/users/{user.id}')
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 200)
      self.assertIn('mahamat', data['data']['username'])
      self.assertIn('mahamat@example.com', data['data']['email'])
      self.assertIn('success', data['status'])

  def test_single_user_no_id(self):
    """Ensure error is thrown if an id is not provided."""
    with self.client:
      response = self.client.get('/users/blah')
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 404)
      self.assertIn('User does not exist', data['message'])
      self.assertIn('fail', data['status'])

  def test_single_user_incorrect_id(self):
    """Ensure error is thrown if the id does not exist."""
    with self.client:
      response = self.client.get('/users/999')
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 404)
      self.assertIn('User does not exist', data['message'])
      self.assertIn('fail', data['status'])

  def test_all_users(self):
    """Ensure get all users behaves correctly."""
    add_user('mahamat1', 'mahamat1@example.com')
    add_user('mahamat2', 'mahamat2@example.com')
    with self.client:
      response = self.client.get('/users')
      data = json.loads(response.data.decode())
      self.assertEqual(response.status_code, 200)
      self.assertEqual(len(data['data']['users']), 2)
      self.assertIn('mahamat1', data['data']['users'][0]['username'])
      self.assertIn('mahamat1@example.com', data['data']['users'][0]['email'])
      self.assertIn('mahamat2', data['data']['users'][1]['username'])
      self.assertIn('mahamat2@example.com', data['data']['users'][1]['email'])
      self.assertIn('success', data['status'])

if __name__ == '__main__':
  unittest.main()
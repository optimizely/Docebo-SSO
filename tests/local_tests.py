# -*- coding: utf-8 -*-

import base64
import datetime
import hashlib
import unittest
import urlparse

from docebo_sso import user
from docebo_sso import methods as docebo_sso


class DoceboUnitTestSso(unittest.TestCase):

  def setUp(self):
    user.initialize_keys(
      domain='http://test.docebosaas.com',
      api_secret='myapisecret',
      api_key='myapikey',
      sso_secret='myssosecret'
    )

  def test_create_datestring(self):
    """Test that the datestring is created correctly"""
    datestring = docebo_sso.create_datestring()
    expected = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    self.assertEqual(len(datestring), 14)
    self.assertAlmostEqual(int(datestring), int(expected))

  def test_create_token(self):
   """Test that SSO token is correctly created """
   username = 'batman'
   datestring = docebo_sso.create_datestring()
   sso_token = docebo_sso.create_token('batman', datestring)
   self.assertEqual(len(sso_token), 32)
   self.assertTrue(isinstance(sso_token, str))

   token_hash = hashlib.md5()
   token_hash.update(username + ',')
   token_hash.update(datestring + ',')
   token_hash.update(docebo_sso.USER_KEYS['sso_secret'])
   expected_token = token_hash.hexdigest()
   self.assertEqual(expected_token, sso_token)

  def test_create_authentication_path(self):
    """Test that SSO path is created correctly for redirect"""
    datestring = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    username = 'batman'
    token = docebo_sso.create_token(username, datestring)
    auth_path = docebo_sso.create_authentication_path(
      username,
      docebo_sso.create_datestring(),
      token
    )
    url_parts = urlparse.urlparse(auth_path)
    self.assertEqual(url_parts.scheme, 'http')
    self.assertEqual(url_parts.netloc, 'test.docebosaas.com')
    self.assertEqual(url_parts.path, '/lms/index.php')

    query_params = url_parts.query.split('&')
    expected_query_params = set([
      'r=site%2Fsso',  # %2F is the urlencoded value of '/'
      'modname=login',
      'op=confirm',
      'login_user=%s' % username,
      'time=%s' % datestring,
      'token=%s' % token
    ])
    for param in query_params:
      self.assertTrue(
        param in expected_query_params,
        msg='Query param "%s" is not in our expected parameter list.' % param
      )

  def test_generate_api_hash(self):
   """Test that the api authentication hash was correctly created"""
   params = {'userid': 'bats'}
   api_hash = docebo_sso.generate_api_hash(params)
   self.assertEqual(len(api_hash), 68)
   self.assertTrue(isinstance(api_hash, str))

  def test_generate_api_hash__unicode(self):
    """ Make sure no errors are raised when using unicode strings with non-ascii chars """
    params = {'userid': u'Renée'}
    api_hash = docebo_sso.generate_api_hash(params)
    self.assertEqual(len(api_hash), 68)
    self.assertTrue(isinstance(api_hash, str))


class DoceboUserTest(unittest.TestCase):

  def init_user(self):
    currUser = user.User(
      userid='batman',
      firstname='bat',
      lastname='man',
      email='bat@bat.bat',
      reg_code='da_batcave',
      role='a bat'
    )
    return currUser

  def test_user_param_init(self):
    """Test that user_param dict is set correctly on constructor"""
    currUser = self.init_user()
    self.assertEqual(currUser.user_params['userid'], 'batman')
    self.assertEqual(currUser.user_params['firstname'], 'bat')
    self.assertEqual(currUser.user_params['lastname'], 'man')
    self.assertEqual(currUser.user_params['email'], 'bat@bat.bat')
    self.assertEqual(currUser.user_params['reg_code'], 'da_batcave')
    self.assertEqual(currUser.user_params['role'], 'a bat')

  def test_add_unique_id(self):
    """Test that unique_id updates correctly on function call"""
    currUser = self.init_user()
    unique_id = 1234
    currUser.set_docebo_unique_id(1234)
    self.assertEqual(currUser.user_params['idst'], '1234')

if __name__ == 'main':
  testmodules = [
    'tests'
  ]
  suite = unittest.TestSuite()

  for t in testmodules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

  unittest.TextTestRunner().run(suite)

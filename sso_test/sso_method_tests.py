import base64
import datetime
import hashlib
import unittest
import urlparse

from doceboSSO import docebo_sso


def __main__():
  testmodules = [
    'sso_method_tests',
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

class DoceboUnitTestSSO(unittest.TestCase):
  current_sso = docebo_sso.DoceboSSO()
  current_sso.initialize_keys(
    domain='http://test.docebosaas.com',
    api_secret='myapisecret',
    api_key='myapikey',
    sso_secret='myssosecret'
  )

  def test_create_datestring(self):
    """Test that the datestring is created correctly"""
    datestring = self.current_sso.create_datestring()
    expected = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    self.assertEqual(len(datestring), 14)
    self.assertAlmostEqual(int(datestring), int(expected))

  def test_create_token(self):
   """Test that SSO token is correctly created """
   username = 'batman'
   datestring = self.current_sso.create_datestring()
   sso_token = self.current_sso.create_token('batman', datestring)
   self.assertEqual(len(sso_token), 32)
   self.assertTrue(isinstance(sso_token, str))

   token_hash = hashlib.md5()
   token_hash.update(username + ',')
   token_hash.update(datestring + ',')
   token_hash.update(self.current_sso.sso_secret)
   expected_token = token_hash.hexdigest()
   self.assertEqual(expected_token, sso_token)

  def test_create_authentication_path(self):
    """Test that SSO path is created correctly for redirect"""
    datestring = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    username = 'batman'
    auth_path = self.current_sso.create_authentication_path(
      username,
      self.current_sso.create_datestring(),
      self.current_sso.create_token(username, datestring)
    )
    url_parts = urlparse.urlparse(auth_path)
    self.assertEqual(url_parts.scheme, 'http')
    self.assertEqual(url_parts.netloc, 'test.docebosaas.com')
    self.assertEqual(url_parts.path, '/doceboLms/index.php')
    queries = url_parts.query.split('&')
    self.assertTrue(queries[0].startswith('login_user'))
    print queries[1]
    self.assertTrue(queries[1] == ('modname=login'))
    self.assertTrue(queries[2].startswith('time'))
    self.assertTrue(queries[3].startswith('token'))
    self.assertEqual(queries[4], 'op=confirm')


  def test_api_hash(self):
   """Test that the api authentication hash was correctly created"""
   params = {'userid': 'bats'}
   api_hash = self.current_sso.generate_api_hash(params)
   self.assertEqual(len(api_hash), 68)
   self.assertTrue(isinstance(api_hash, str))

   param_string = ','.join(params.values())
   secret_hash = hashlib.sha1(param_string + ',' + self.current_sso.api_secret)
   auth_token = base64.b64encode(self.current_sso.api_key + ':' + secret_hash.hexdigest())
   self.assertEqual(auth_token, api_hash)

class DoceboUserTest(unittest.TestCase):

  def init_user(self):
    currUser = DoceboUser.SSOUser(
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

  def test_update_user_params(self):
    """Test that user params are updated correctly on local User copy"""
    currUser = self.init_user()
    currUser.update_info_locally(
      firstname='bruce',
      lastname='wayne'
    )
    self.assertEqual(currUser.user_params['firstname'], 'bruce')
    self.assertEqual(currUser.user_params['lastname'], 'wayne')
    self.assertEqual(currUser.user_params['userid'], 'batman')

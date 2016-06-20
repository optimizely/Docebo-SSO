import copy
import logging

import methods as docebo_sso

logger = logging.getLogger(__name__)

possible_edit_fields = [
  'idst',
  'ext_user_type',
  'ext_user',
  'firstname',
  'lastname',
  'password',
  'email',
]

possible_create_fields = [
  'userid',
  'firstname',
  'lastname',
  'password',
  'email',
  'reg_code',
  'reg_code_type',
  'ext_user_type',
  'ext_user',
  'role',
  'language',
  'orgchart'
]

possible_delete_fields = [
  'idst',
  'ext_user_type',
  'ext_user'
]

possible_verify_fields = [
  'userid'
]


def initialize_keys(domain, api_secret, api_key, sso_secret):
  docebo_sso.USER_KEYS['domain'] = domain
  docebo_sso.USER_KEYS['api_secret'] = api_secret
  docebo_sso.USER_KEYS['api_key'] = api_key
  docebo_sso.USER_KEYS['sso_secret'] = sso_secret


class User(object):

  def __init__(self, userid, **kwargs):
    """Definition of all characteristics assigned with the given user, stores input as an object field

    All Docebo user traits can be found at https://www.docebo.com/wp-content/uploads/media/Docebo_APImanual.pdf

    args: all appropriate user fields (with username required)
    """
    self.user_params = copy.deepcopy(kwargs)
    self.user_params['userid'] = userid

  def set_docebo_unique_id(self, unique_id):
    """Allows Docebo unique user id to be defined."""
    self.user_params['idst'] = str(unique_id)

  def generate_params(self, possible_fields):
    """returns dict of appropriate params for user deletion"""
    return {
      field: self.user_params[field] for field in possible_fields
      if field in self.user_params
    }

  def exists(self):
    """Verify whether user already exists in Docebo system

    returns: boolean for user found
    """
    params = self.generate_params(possible_verify_fields)
    verify_response = docebo_sso.verify_user(params)
    did_succeed = verify_response['success']
    if did_succeed:
      self.set_docebo_unique_id(str(verify_response['idst']))
    return did_succeed

  def create(self):
    """Creates user with traits as specified

    returns: boolean for success"""
    params = self.generate_params(possible_create_fields)
    create_response = docebo_sso.create_user(params)
    if not create_response:
      return False
    self.set_docebo_unique_id(str(create_response['idst']))
    return create_response['success']

  def delete(self):
    """ deletes user specified by user_id provided

    ***MUST RUN verify_existence() or set_docebo_unique_id() BEFORE RUNNING delete()***

    return: boolean for success
    """
    if 'idst' not in self.user_params:
      logger.error('Docebo user unique ID not initialized.')
      return False

    params = self.generate_params(possible_delete_fields)
    return docebo_sso.delete_user(params)['success']

  def update(self):
    """updates a docebo user with parameters specified in creating the object

    ***MUST RUN verify_existence() or set_docebo_unique_id() BEFORE RUNNING delete()***

    return: boolean value for success or not
    """
    if 'idst' not in self.user_params:
      logger.error('Docebo user unique ID not initialized')
      return False
    params = self.generate_params(possible_edit_fields)
    return docebo_sso.edit_user(params)['success']

  def signin(self):
    """Provides the signed and paramterized URL to sign into an active Docebo account

    returns: URL as a string
    """
    username = self.user_params['userid']
    return docebo_sso.setup_valid_docebo_sso_path_and_params(username)

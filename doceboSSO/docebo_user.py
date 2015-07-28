from doceboSSO import docebo_sso


class SSOUser(docebo_sso.DoceboSSO):

  def __init__(self, userid, **kwargs):
    """Definition of all characteristics assigned with the given user, stores input as an object field

    All Docebo user traits can be found at https://www.docebo.com/wp-content/uploads/media/Docebo_APImanual.pdf

    args: all appropriate user fields (with username required)
    """
    self.user_params = kwargs
    self.user_params['userid'] = userid

  def set_docebo_unique_id(self, unique_id):
    """Allows Docebo unique user id to be defined."""
    self.user_params['idst'] = str(unique_id)

  def generate_user_verify_params(self):
    """returns dict of appropriate params for user verification"""
    params = {
      'userid': self.user_params['userid'],
      'also_check_as_email': 'false'
    }
    return params

  def generate_user_edit_params(self):
    """returns dict of appropriate params for user updating"""
    return self.user_params

  def generate_user_creation_params(self):
    """returns dict of appropriate params for user creation"""
    return self.user_params

  def generate_delete_user_params(self):
    """returns dict of appropriate params for user deletion"""
    return self.user_params

  def verify_existence(self):
    """Verify whether user already exists in Docebo system

    returns: boolean for user found
    """
    params = self.generate_user_verify_params()
    verify_response = self.verify_user(params)
    did_succeed = verify_response['success']
    if did_succeed:
      self.set_docebo_unique_id(str(verify_response['idst']))
    return did_succeed

  def create(self):
    """Creates user with traits as specified

    returns: boolean for success"""
    params = self.generate_user_creation_params()
    create_response = self.create_user(params)
    if not create_response:
      return False
    self.set_docebo_unique_id(str(create_response['idst']))
    return create_response

  def delete(self):
    """ deletes user specified by user_id provided

    ***MUST RUN verify_existence() or set_docebo_unique_id() BEFORE RUNNING delete()***

    return: boolean for success
    """

    if not 'idst' in self.user_params:
      return False

    params = self.generate_delete_user_params()
    return self.delete_user(params)['success']

  def update_on_docebo(self):
    """updates a docebo user with paramters specified in creating the object

    ***MUST RUN verify_existence() or set_docebo_unique_id() BEFORE RUNNING delete()***

    return: boolean value for success or not
    """
    if not 'idst' in self.user_params:
      return False
    params = self.generate_user_edit_params()
    return self.edit_user(params)['success']

  def signin(self):
    """Provides the signed and paramterized URL to sign into an active Docebo account

    returns: URL as a string
    """
    username = self.user_params['userid']
    return self.setup_valid_sso_path_and_params(username)

  def update_info_locally(self, **kwargs):
    """Updates info for a user locally (in the DoceboUser object). Does overwrite values.

    args: fields and values to be updated
    """
    self.user_params.update(kwargs)




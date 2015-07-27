Docebo-SSO
==========

This package is meant to allow a simple python interface to add a third
party Single Sign On to the Docebo Learning Management System. Docebo's
SSO does not create a user that doesn't exist, or update the credentials
of a user that does exist.

Usage
-----

There are two ways to use this package, depending on the amount of
customization that you need with Docebo's sign on.

User API
~~~~~~~~

The user API is a simple, flexible set of methods to sync a Docebo user
with a locally created user object. To ue the methods, the DoceboUser
object must first be instantiated with all of the information to be
synced with the user from Docebo

A full list of valid user parameters can be found at Docebo's API
reference:
https://www.docebo.com/wp-content/uploads/media/Docebo\_APImanual.pdf

.. code:: sh

    from SSO_libs import docebo_user

    new_user = DoceboUser(
     userid='batman',
     firstname='john',
     lastname='Doe',
     ...
    )

Next, the API and SSO keys and the hosting domain for your LMS must be
initialized. This method will also create the appropriate hashes and
tokens necessary for using Docebo's API

.. code:: sh

    new_user.initialize_keys(
     domain='http://example.docebosaas.com'
     api_key='xxxxxxxxxx'
     api_secret='xxxxxxxxxx'
     sso_token='xxxxxx'
    )

Finally, you can use the methods in the DoceboUser api to interact with
Docebo -- the methods use the parameters you input into the DoceboUser
object and generate valid params/api\_keys.

.. code:: sh

    if new_user.verify_existence():
      new_user.update_on_docebo()
    else:
      new_user.create()

    redirect_url = new_user.signin()

The above is a simple script to create the local user initialized in the
first step if their userid doesn't exist on Docebo, and update their
user parameters if they do exist.

redirect\_to will contain a valid, signed, URL to signin to that user's
account on Docebo that can be redirected to or pasted into a browser.

The following call can also be used to update the specified user
attributes on the local DoceboUser. This info can then be pushed to
Docebo/used to create a new user.

.. code:: sh

    new_user.update_info_locally(
      firstname='jane',
      lastname='dae',
      ...
    )

Available methods are:

.. code:: sh

    All of these methods return boolean values for success for easy control flow

    from SSO_libs import docebo_user

    # Initialize user object with keys, secrets and domain
    initialize_keys(self, domain, api_secret, api_key, sso_secret)

    # Verify user exists in Docebo
    # Hits /api/user/checkUsername
    verify_existence(self)

    # Update remote user params given local user information
    update_on_docebo(self)

    # Create a new user based on local user 
    # Hits /api/user/create
    create(self)

    # Delete user
    # Hits /api/user/delete
    delete(self)

    # Sign user in (if account exists), and return URL which will sign that user into their docebo account
    signin(self)

    # Update local user's information
    update_info_locally

In order to call delete or update\_on docebo, the docebo unique-id for that given user is required.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

create() and verify\_existence() automatically add this field on success
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use the following method to add the uid manually.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

    new_user.set_docebo_unique_id(#####)

Methods API
^^^^^^^^^^^

The second method of interaction is less abstracted, but gives the user
more control over the params. Where the User API generates params and
fills in information for the user, the Methods API requires the user to
input a set of params as a dictionary at every call.

The correct format for the params generated for each method can be found
at:
https://www.docebo.com/wp-content/uploads/media/Docebo\_APImanual.pdf

The api\_key, api\_secret and sso\_secret must still be initialized as
in the User API.

Available methods are:

.. code:: sh

    These methods return the json body of the responses they receive.

    # Verify user exists in Docebo
    verify_user(self, params)

    # Update user params w/input params
    edit_user(self, params)

    # Create a new user given input params
    # If called on a user that already exists, returns None
    create_user(self, params)

    # Delete user corresponding to provided unique_id
    delete_user(self, params)

    # Sign user in (if account exists), and return URL which will sign that user into their docebo account
    setup_valid_sso_path_and_params(self, username)

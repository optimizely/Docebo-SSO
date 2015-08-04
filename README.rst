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
with a locally created user object. To ue the methods, the User object
must first be instantiated with all of the information to be synced with
the user from Docebo

A full list of valid user parameters can be found at Docebo's API
reference:
https://www.docebo.com/wp-content/uploads/media/Docebo\_APImanual.pdf

.. code:: sh

    from docebo_sso import user as docebo_user

    new_user = docebo_user.User(
     userid='batman',
     firstname='john',
     lastname='Doe',
     ...
    )

Next, the API and SSO keys and the hosting domain for your LMS must be
initialized. This method will also create the appropriate hashes and
tokens necessary for using Docebo's API

.. code:: sh

    docebo_user.initialize_keys(
     domain='http://example.docebosaas.com'
     api_key='xxxxxxxxxx'
     api_secret='xxxxxxxxxx'
     sso_token='xxxxxx'
    )

Finally, you can use the methods in the User api to interact with Docebo
-- the methods use the parameters you input into the User object and
generate valid params/api\_keys.

.. code:: sh

    if new_user.exists():
      new_user.update()
    else:
      new_user.create()

    redirect_url = new_user.signin()

The above is a simple script to create the local user initialized in the
first step if their userid doesn't exist on Docebo, and update their
user parameters if they do exist.

redirect\_url will contain a valid, signed, URL to signin to that user's
account on Docebo that can be redirected to or pasted into a browser.

Available methods are:

.. code:: sh

    All of these methods return boolean values for success for easy control flow

    from docebo_sso import user as docebo_user

    # Initialize user object with keys, secrets and domain
    docebo_user.initialize_keys(self, domain, api_secret, api_key, sso_secret)

    # Verify user exists in Docebo (by username)
    # Hits /api/user/checkUsername
    exists(self)

    # Update remote user params from local user information
    update(self)

    # Create a new user based on local user 
    # Hits /api/user/create
    create(self)

    # Delete user
    # Hits /api/user/delete
    delete(self)

    # Sign user in (if account exists), and return URL which will sign that user into their docebo account
    signin(self)

In order to call delete or update, the docebo unique-id for that given user is required.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

create() and exists() automatically add this field on success
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use the following method to add the uid manually.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

    new_user.set_docebo_unique_id(#####)

Methods API
^^^^^^^^^^^

The second method of interaction is less abstracted, but gives more
control over the params. Where the User API generates params and fills
in information for the user, the Methods API requires the user to input
a set of params as a dictionary at every call.

The correct format for the params generated for each method can be found
at:
https://www.docebo.com/wp-content/uploads/media/Docebo\_APImanual.pdf

The api\_key, api\_secret and sso\_secret must still be initialized as
in the User API.

Available methods are:

.. code:: sh

    from docebo_sso import methods as docebo_methods

    #These methods return the json body of the responses they receive.

    # Verify user exists in Docebo
    docebo_methods.verify_user(self, params)

    # Update user params w/input params
    docebo_methods.edit_user(self, params)

    # Create a new user given input params
    # Gives an 'empty response' error if user already exists
    docebo_methods.create_user(self, params)

    # Delete user corresponding to provided unique_id
    docebo_methods.delete_user(self, params)

    # Sign user in (if account exists), and return URL which will sign that user into their docebo account
    docebo_methods.setup_valid_docebo_sso_path_and_params(self, username)

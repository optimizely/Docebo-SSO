# Docebo-SSO
This package is meant to allow a simple python interface to add a third party Single Sign On to the Docebo Learning Management System

## Usage

There are two ways to use this product, depending on the amount of customization that you need with Docebo.

#### User API

The user API is a simple, flexible set of methods to sync a Docebo user with a locally created user object.
To ue the methods, the DoceboUser object must first be instantiated with all of the information to be synced with the user from Docebo

A full list of valid user parameters can be found at Docebo's API reference: https://www.docebo.com/wp-content/uploads/media/Docebo_APImanual.pdf
```sh
new_user = DoceboUser(
 userid='batman',
 firstname='john',
 lastname='Doe',
 ...
)
```
Next, the API and SSO keys and the hosting domain for your LMS must be initialized. This method will also create the appropriate hashes and tokens necessary for using Docebo's API
```sh
new_user.initialize_keys(
 domain='http://example.docebosaas.com'
 api_key='xxxxxxxxxx'
 api_secret='xxxxxxxxxx'
 sso_token='xxxxxx'
)
```
Finally, you can use the methods in the DoceboUser api to interact with Docebo -- using the parameters you input into the DoceboUser object.
```sh
if new_user.verify_existence():
  new_user.update_on_docebo()
else:
  new_user.create()

redirect_url = new_user.signin()
```
The above is a simple script to create the local user initialized in the first step if their userid doesn't exist on Docebo, and update their user parameters if they do exist. 

redirect_to will contain a valid, signed, URL to signin to that user's account on Docebo that can be redirected to or pasted into a browser.

The following call can also be used to update the specified user attributes on the local DoceboUser. This info can then be pushed to Docebo/used to create a new user.

```sh
new_user.update_info_locally(
  firstname='jane',
  lastname='dae',
  ...
)

Available methods are:
```sh
# Initialize user object with keys, secrets and domain
initialize_keys(self, domain, api_secret, api_key, sso_secret)

# Verify user exists in Docebo
verify_existence(self)

# Update remote user params given local user information
update_on_docebo(self)

# Create a new user based on local user 
create(self)

# Delete user
delete(self)

# Sign user in (if account exists), and return URL which will sign that user into their docebo account
signin(self)

# Update local user's information
update_info_locally
```

```
####NOTE: A user must be verified to exist (using verify_existence) or have been created by this package to succesfully call 'delete' or 'update_on_docebo', even if the user does already exist.
### If you know the Docebo Unique ID ('idst') for the user, you can also use 
```sh
new_user.set_docebo_unique_id(1234)
```

#### Methods API

The second method of interaction is less abstracted, but gives the user more control over the params.
Where the User API generates params and fills in information for the user, the Methods API requires the user to input a set of params as a dictionary at every call.

The correct format for the params generated for each method can be found at: https://www.docebo.com/wp-content/uploads/media/Docebo_APImanual.pdf

The api_key, api_secret and sso_secret must still be initialized as in the User API. 

Available methods are: 
```sh
# Verify user exists in Docebo
verify_user(self, params)

# Update user params w/input params
edit_user(self, params)

# Create a new user given input params
create_user(self, params)

# Delete user corresponding to provided unique_id
delete_user(self, params)

# Sign user in (if account exists), and return URL which will sign that user into their docebo account
setup_valid_sso_path_and_params(self, username)
```




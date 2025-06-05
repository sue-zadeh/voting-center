"""Script to generate password hashes for one or more user accounts.

You can use this script to generate flask_hashing password hashes for all of
the initial user accounts in your database creation script. Remember that each
of your user accounts should have its own unique password.

You'll need to make two changes before running this script:

1.  Replace the value of constant PASSWORD_SALT, 'ExampleSaltValue', with
    whateveer salt value you're using in your web app.

2.  Replace the list of user accounts (the block beginning "users = [") with
    the actual list of user accounts you need to generate hashes for.
"""
from collections import namedtuple
from flask import Flask
from flask_hashing import Hashing

# IMPORTANT: Change 'ExampleSaltValue' to whatever salt value you'll use in
# your application. If you don't do this, your password hashes won't work!
PASSWORD_SALT = '1234abcd'
# We use a "named tuple" here to create a simple "User Account" class that can
# store a username and password.
# 
# Don't worry if you haven't seen this before: it's just a simple way of
# storing those two pieces of data together in one variable. It also lets us
# access the username and password by name: for example, if we create a
# UserAccount named "myuser", like this:
# 
# myuser = UserAccount('myusername', 'mypassword')
# 
# We can then access those values via "myuser.username" and "myuser.password",
# instead of having to access myuser[0] and myuser[1] like you would have to
# with a regular tuple.
UserAccount = namedtuple('UserAccount', ['username', 'password'])

app = Flask(__name__)
app.secret_key = 'e2e62cdb171271f0b12e5043f9f84208eba1f05c8658704e'
hashing = Hashing(app)

# Replace the example UserAccount objects below with the initial user accounts
# for your own web app. You can add as many as you need to the list.
users = [UserAccount('user1', 'user1pass'), 
         UserAccount('user2', 'user2pass'),
         UserAccount('user3', 'user3pass'),
         UserAccount('user4', 'user4pass'),
         UserAccount('user5', 'user5pass'),
         UserAccount('user6', 'user1pass'), 
         UserAccount('user7', 'user2pass'),
         UserAccount('user8', 'user3pass'),
         UserAccount('user9', 'user4pass'),
         UserAccount('user10', 'user5pass'),
         UserAccount('user11', 'user1pass'), 
         UserAccount('user12', 'user2pass'),
         UserAccount('user13', 'user3pass'),
         UserAccount('user14', 'user4pass'),
         UserAccount('user15', 'user5pass'),
         UserAccount('user16', 'user1pass'), 
         UserAccount('user17', 'user2pass'),
         UserAccount('user18', 'user3pass'),
         UserAccount('user19', 'user4pass'),
         UserAccount('user20', 'user5pass'),
         UserAccount('user21', 'user4pass'),
         UserAccount('user22', 'user5pass'),
         UserAccount('user225', '123Suezx.'),
         
         
         UserAccount('moderator1', 'moderator1pass'),
         UserAccount('moderator2', 'moderator2pass'),
         UserAccount('moderator3', 'moderator1pass'),
         UserAccount('moderator4', 'moderator2pass'),
         UserAccount('moderator5', 'moderator1pass'),
         UserAccount('moderator6', 'moderator2pass'),
         UserAccount('moderator7', 'moderator1pass'),
         UserAccount('moderator8', 'moderator2pass'),
         UserAccount('user400', '123Suezx.'),

         
         UserAccount('admin1', 'admin1pass'),
         UserAccount('admin2', 'admin1pass'),
         UserAccount('admin3', 'admin1pass'),
         UserAccount('admin4', 'admin1pass'),
         UserAccount('user901', '123Suezx.')] 



print('Username | Password | Hash | Password Matches Hash')

for user in users:
    # Generate a SHA-256 hash using the default settings for flask_hashing and
    # the salt value we defined earlier. This function returns the hash as a 64
    # character string in hexadecimal.
    password_hash = hashing.hash_value(user.password, PASSWORD_SALT)
     
    # Check whether the hash matches the original password. We don't really
    # need to do this here: this is just to show how your web app would check a
    # password supplied by the user (user.password) against a hash value
    # retrieved from the database (password_hash). Note that your application's
    # salt value is also required when checking a password.
    # 
    # This returns True if the password matches, or False if it doesn't.
    password_matches_hash = hashing.check_value(password_hash, user.password, PASSWORD_SALT)

    # Output username, password, hash, and the result of our verification test.
    # 
    # Note that username is never actually used when generating the hash or
    # checking a password. We only include username here for display purposes,
    # to make it easier for you to copy the right password for each user when
    # creating your database population script.
    print(f'{user.username} | {user.password} | {password_hash} | {password_matches_hash}')
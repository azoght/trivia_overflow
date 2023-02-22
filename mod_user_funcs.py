'''
Functions that allow admins to modify verified users in one of two ways

Deleting any verified user automatically from the application
Promoting any qualified (level 10 or above) user to an admin
'''

from test_users import *

def delete_user(username): # removes a verified user 
  test_verified.pop(username)
  all_usernames.remove(username)

def promote_user(username): # promotes a qualified verified user to admin 
  test_admins[username] = dict()
  for key in list(test_verified[username].keys()):
    test_admins[username][key] = test_verified[username][key]
  test_verified.pop(username)
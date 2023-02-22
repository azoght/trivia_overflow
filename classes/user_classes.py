'''
Classes representing the three types of users for this application

Guests are free to browse around but can't use most services
Verified users have created an account and can use most services
Admins are experienced users who can create questions and manage verified users
'''

class User: # what all users should have
  
  def __init__(self, name):
    self.name = name
    self.password = ""
    self.permissions = []

class Guest(User):

  def __init__(self):
    self.name = "Guest"
    self.password = ""
    self.permissions = []

  def __repr__(self):
    return "guest"

class Verified(User):
  
  def __init__(self, name, password, posts_responded_to=[], posts_rewarded_for=[], points=0, progress=0):
    self.name = name
    self.password = password
    self.permissions = [
      'answer_questions', 
      'earn_points',
      'virtual_shop',
    ]
    self.posts_responded_to = posts_responded_to # a list of ids of the posts that user responds to
    self.posts_rewarded_for = posts_rewarded_for # a list of ids of the posts that user is rewarded for
    self.points = points # these are earned through various actions, such as getting 
    self.progress = progress # keeps track of points the user earned to help determine level

  def get_level(self): # returns the level based on the number of progress points user has
    return int((-90 + (8100 + (40 * self.progress)) ** 0.5) / 20)

  def __repr__(self):
    return "verified"

class Admin(User):
  
  def __init__(self, name, password, posts_responded_to=[], posts_rewarded_for=[], points=0):
    self.name = name
    self.password = password
    self.permissions = [
      'answer_questions',
      'post_questions',
      'earn_points',
      'modify_games',
      'virtual_shop',
      'modify_users'  # and questions too...coming soon...
    ]
    self.posts_responded_to = posts_responded_to
    self.posts_rewarded_for = posts_rewarded_for 
    self.points = points

  def __repr__(self):
    return "admin"

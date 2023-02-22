'''
Dictionaries containing test admin and verified user information
'''

from crypt_funcs import encrypt_password

test_admins = {
  'TriviaMaster1': {
    'password': encrypt_password('sussussus'),
    'points': 80, 
    'posts_responded_to': [],
    'posts_rewarded_for': []
  },
  'Loca4Trivia': {
    'password': encrypt_password('t3guHEaLYW'), 
    'points': 130, 
    'posts_responded_to': [],
    'posts_rewarded_for': []
  }
}

test_verified = {
  'Contento2': {
    'password': encrypt_password('y6Dw4h5E3a'),
    'points': 100,
    'progress': 1000,
    'posts_responded_to': [],
    'posts_rewarded_for': []
  },
  'DasMickey5': {
    'password': encrypt_password('r8CG6zkEeV'),
    'points': 65,
    'progress': 800,
    'posts_responded_to': [],
    'posts_rewarded_for': []
  },
  'TerraCotta3': {
    'password': encrypt_password('3mgACdCSxD'),
    'points': 200,
    'progress': 1950, 
    'posts_responded_to': [],
    'posts_rewarded_for': []
  },
  'Gurlynx4': {
    'password': encrypt_password('pkpmY2jUhe'),
    'points': 300,
    'progress': 500, 
    'posts_responded_to': [],
    'posts_rewarded_for': []
  }
}

other_usernames = ['SoccerBuff7', 'NickTheTrick0', 'Epic36', 'DudeSpoiled99', 'A1iceInSlumberland', 'b0b']

all_usernames = list(test_admins.keys()) + list(test_verified.keys()) + other_usernames # list of all registered ("taken") usernames
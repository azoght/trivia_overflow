'''
Encryption and decryption of passwords

Instead of simpler ciphers, this program uses the cryptography.fernet module (which is not built in to Python, so it must be installed)

Fernet is an implementation of symmetric cryptography, meaning that the material to be encrypted or decrypted requires a secret key to do so.

Each time this program is ran, a new key is generated and stored in the file "secret.key" (though I might change this so that the same key is used every time, it will be easier if all the user information is stored permanently upon creation). 

Initially, each user's password is encrypted with this key. This is also done when a new user signs up. Once a user logs in, the decrypted version of the user's stored password is compared with that which was typed in. If they match, the password remains encrypted and the user is successfully logged in. If not, they are warned.
'''

import cryptography.fernet as crypt 

def generate_key(): # generates a key to save into a file
  key = crypt.Fernet.generate_key()
  with open("secret.key", "wb") as f:
    f.write(key)

generate_key()

def load_key(): # loads the previously generated key
  return open("secret.key", "rb").read()

def encrypt_password(password):
  key = load_key()
  encoded_password = password.encode()
  f = crypt.Fernet(key)
  encyrpted_password = f.encrypt(encoded_password)
  
  return encyrpted_password

def decrypt_password(password):
  key = load_key()
  f = crypt.Fernet(key)
  decrypted_password = f.decrypt(password)

  return decrypted_password.decode()
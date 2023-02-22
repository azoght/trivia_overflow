# trivia_overflow
A forum (almost) entirely dedicated to trivia, where some users can post questions, while others answer to earn points


## Installation Instructions
Before you run this program from IDLE or any other IDE, open your favorite terminal application, go to the directory of this file and run the following:

```bash
pip install -r requirements.txt
```

Now that the dependency is installed, run your IDE again, open 'main.py' and run it


## Directory
* constants.py: values that remain constant throughout GUI
* crypt_funcs.py: cryptography-related functions that help encrypt and decrypt users' passwords
* mod_user_funcs.py: functions only admin users have access to that allow them to modify verified users
* posts_responses.py: all the initial posts and responses
* test_users.py: all initial admins and verified users
* user_funcs.py: functions that help users navigate the GUI and process their information, including the many pages of this program
* other_funcs.py: any other functions used in this program
* classes: all classes representing users and componnents
   * trivia_classes.py: contains all classes related to the trivia aspect of this program, question, post, response, and OpenTrivia Database Faucet
   * user_classes.py: contains all classes representing the different types of users in this service, guest, verified, and admin
* games: the additional componnents of this project

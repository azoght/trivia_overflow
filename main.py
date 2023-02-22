'''
Name: TriviaOverflow Message Board
Author: Angelina Zoght
Date: April 8, 2022
Description: a forum almost entirely dedicated to trivia, where some users can post questions, while others answer to earn points
'''

'''
*Installation Instructions:*

Before you run this program from IDLE, please open your favorite terminal application, go to the directory of this file and run the following:
$ pip install -r requirements.txt

Now that the dependency is installed, run IDLE and open 'main.py' and run it
'''

'''
*Directory:*

constants.py: contains values that remain constant throughout GUI
crypt_funcs.py: contains cryptography-related functions that help encrypt and decrypt users' passwords
mod_user_funcs.py: contains functions only admin users have access to that allow them to modify verified users
posts_responses.py: contains all the initial posts and responses
test_users.py: contains all the initial admins and verified users
user_funcs.py: contains functions that help users navigate the GUI and process their information, including the many pages of this program
other_funcs.py: contains any other functions used in this program
classes: all the classes representing users and componnents
    trivia_classes.py: contains all classes related to the trivia aspect of this program, question, post, response, and OpenTrivia Database Faucet
     user_classes.py: contains all classes representing the different types of users in this service, guest, verified, and admin
games: the additional componnents of this project
'''

from tkinter import * # for GUI

# imports from other files in this repository

from user_funcs import *

HEIGHT = 400
WIDTH = 800
BG_COLOR = '#b8f5ed'

# set up window

win = Tk()
win.geometry(f"{WIDTH}x{HEIGHT}") # set dimensions
win.configure(bg=BG_COLOR)

Label(win, text='TRIVIA OVERFLOW', bg=BG_COLOR, font=('Helvetica', 40)).place(x=WIDTH/2, y=35, anchor='c') # title for all pages, space must be created


home_page(win, {})

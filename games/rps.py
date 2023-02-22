"""
Plays "Rock, Paper, Scissors" with a computer, where "easy" mode is Part 1, "medium" mode is Part 3, and "hard" mode is Part 2


User Permissions:
Guests can play "easy" mode only for 1 to 3 rounds
Verifieds can play "easy" and "hard" modes for any number of rounds and pay 10 points to play "medium" mode
Admins have access to every feature of the game for free

If Verifieds or Admins win a game, they will earn 20 points
"""

from tkinter import *  # tkinter widgets
from PIL import Image, ImageTk # for images; install pillow first
from tkinter.font import Font  # for fonts
import random  # for randomization of choice

# imports from outside directory
import sys
import os
sys.path.append(os.path.join("..", 'classes'))

from classes.user_classes import *

# colours

GRAY = '#a0a0a0'
BLACK = '#000000'
WHITE = '#ffffff'
GREEN = '#0a8c0a'
RED = '#8c0a0a'
BLUE = '#0a0a8c'

class Hand: # class representing displayed player's hand

  def __init__(self, frame, filename):
    if filename != None:
      self.image = ImageTk.PhotoImage(Image.open("images/"+filename+".gif").resize((120,120)))
    else:
      self.image = None
    self.label = Label(frame, bg=GRAY, image=self.image)

  def configure_img(self, filename):
    self.image = ImageTk.PhotoImage(Image.open("images/"+filename+".gif").resize((120,120)))
    self.label.configure(image=self.image)
    self.label.image = self.image

def launch_rps(user):
  global round_info
  global win_or_lose
  global your_hand
  global computer_hand
  global choices
  global your_score
  global computer_score
  global start_button
  global hands_frame
  
  # the screen
  root = Toplevel()
  root.title("Rock, Paper, Scissors")
  root.geometry("800x600")  # window size
  root.configure(bg=GRAY)
  
  win = Canvas(root, bg=GRAY)
  win.pack()
  
  # variables
  your_choice = ""
  rounds_var = IntVar()  # determines number of rounds based on dropdown selection
  rounds_var.set("")  # leaves dropdown blank
  modes_var = StringVar()  # determines game mode based on dropdown selection
  modes_var.set("")
  game_mode = ""
  total_rounds = 0
  rounds_remaining = 0
  rounds_won = 0
  rounds_lost = 0
  font = Font(family='Modern', size=15)
  choices = ['rock', 'paper', 'scissors']
  
  # components/widgets (from top to bottom)
  score_board = Frame(win)   # will display the scores of user and computer
  score_board.pack()

  your_score = Label(score_board, text="You:                                 ", fg=BLACK, bg=GRAY, font=font)  # displays the number of games the user has won
  your_score.pack(side=LEFT)
  
  computer_score = Label(score_board, text="Computer: ", fg=BLUE, bg=GRAY, font=font)  # displays the number of games the user has lost
  computer_score.pack(side=RIGHT)

  top_message = Label(win, text="Let's play!\n", fg=BLACK, bg=GRAY, font=font)
  top_message.pack()

  buttons_frame = Frame(win)
  buttons_frame.pack()

  rock_button = Button(buttons_frame, text='Rock', command=lambda: play_game('rock', user), width=10, height=3, fg=BLACK, font=font)  # button to select 'rock' 
  rock_button.pack(side=LEFT)  # goes at the the left
  
  paper_button = Button(buttons_frame, text='Paper', command=lambda: play_game('paper', user), width=10, height=3, fg=BLACK, font=font)  # button to select 'paper'
  paper_button.pack(side=LEFT)  # goes right to the rock button
  
  scissors_button = Button(buttons_frame, text='Scissors', command=lambda: play_game('scissors', user), width=10, height=3, fg=BLACK, font=font)  # button to select 'scissors'
  scissors_button.pack(side=LEFT)  # goes right to the scissors button

  divider = Label(win, text="\n", bg=GRAY, font=('Modern', 3))  # division between choice buttons and dropdowns
  divider.pack()

  modes_frame = Frame(win, bg=GRAY)  # frame that contains the game mode label and dropdown
  modes_frame.pack()

  if repr(user) == "guest":
    modes_options = ["easy"]  # guests can only play 'easy mode' games
  else:
    modes_options = ["easy", "medium", "hard"]  
  modes_select = OptionMenu(modes_frame, modes_var, *modes_options)  # dropdown to select game mode
  modes_menu = root.nametowidget(modes_select.menuname) 
  modes_menu.configure(font=font)
  modes_select.pack(side=RIGHT)
  
  modes_label = Label(modes_frame, text="Game Mode: ", fg=BLACK, bg=GRAY, font=font)
  modes_label.pack(side=RIGHT)

  rounds_frame = Frame(win, bg=GRAY)  # frame that contains the number of rounds label and dropdown
  rounds_frame.pack()  # goes above the start button

  if repr(user) == "guest":
    rounds_options = [1, 3] # guests can play only 1 or 3 rounds per game
  else:
    rounds_options = [1, 3, 5, 7]  # user can play either 1, 3, 5, or 7 rounds
  rounds_select = OptionMenu(rounds_frame, rounds_var, *rounds_options)  # dropdown to select desired number of rounds
  rounds_menu = root.nametowidget(rounds_select.menuname) # to change font
  rounds_menu.configure(font=font)
  rounds_select.pack(side=RIGHT) # goes on the right of the rounds frame
  
  rounds_label = Label(rounds_frame, text='Number of Rounds:', fg=BLACK, bg=GRAY, font=font)
  rounds_label.pack(side=RIGHT)  # goes left to the rounds dropdown
  
  bottom_frame = Frame(win, bg=GRAY) # frame that contains the game mode and number of rounds dropdowns, as well as the start button
  bottom_frame.pack(side=BOTTOM) # goes at the bottom, obviously
  
  start_button = Button(bottom_frame, text="Start Game!", command=lambda:start_game(user, rounds_var, modes_var), fg=BLACK, font=font) # button clicked to start a game
  start_button.pack(side=BOTTOM)  # goes at the bottom of the bottom frame
  
  round_info = Message(root, text="\n\n\n", width=1200, justify=CENTER, fg=BLACK, bg=GRAY, font=font)  # gives info about the current round
  round_info.pack()
  
  hands_frame = Frame(root, bg=GRAY)  # to contain images of the hands played
  hands_frame.pack()  # to be slightly lower than round_info
  
  your_hand = Hand(hands_frame, None)  # displays the move the user plays in a round
  your_hand.label.pack(side=LEFT)  # goes on the left of the hands_frame
  
  computer_hand = Hand(hands_frame, None)  # displays the move the computer plays in a round
  computer_hand.label.pack(side=RIGHT)  # goes on the right of the hands_frame
  
  win_or_lose = Message(root, width=1200, justify=CENTER, font=font, bg=GRAY)  # displays the outcome at the end of the game
  win_or_lose.pack(side=TOP)  # to be slightly lower than images_frame
  
  mainloop()


# function for user to input their choice and play a round
def play_game(choice, user):
    global your_choice
    global choices
    global total_rounds
    global rounds_remaining
    global rounds_won
    global rounds_lost
    global game_mode
    global round_info
    global your_hand
    global computer_hand
  
    mode = game_mode
    r = rounds_remaining
    tr = total_rounds

    # just so that game stops working when rounds are up
    if rounds_remaining == 0:
        round_info.configure(text="\nThere is no game, please use the dropdowns and buttons to start one")
        win_or_lose.configure(text="") 
        return  # 'naked' return ends function

    your_choice = choice

    if mode == 'easy' or (mode == "medium" and r == tr):  # will also run in 'medium' mode for the 1st round
        computer_choice = random.choice(choices)
    elif mode == 'hard' or (mode == "medium" and r != tr):  # will also run in 'medium' mode for 2nd round and beyond
        if your_choice == 'rock':
            computer_choice = 'paper'
        elif your_choice == 'paper':
            computer_choice = 'scissors'
        elif your_choice == 'scissors':
            computer_choice = 'rock'
    else:
        round_info.configure(text="\nInvalid mode, sorry!")
        return

    # final text displayed closer to center
    round_text = f"\nRound {tr - r + 1} of {tr}\n\n"  # keeps track of rounds

    # add choices to text
    round_text += f"You selected: {your_choice}\n"
    round_text += f"Computer selected: {computer_choice}\n"

    # display moves in hands_frame
    if your_choice == 'rock':
        your_hand.configure_img('rock_hand')
    elif your_choice == 'paper':
        your_hand.configure_img('paper_hand')
    elif your_choice == 'scissors':
        your_hand.configure_img('scissors_hand')

    # computer's hand is reversed
    if computer_choice == 'rock':
        computer_hand.configure_img('rock_hand_rev')
    elif computer_choice == 'paper':
        computer_hand.configure_img('paper_hand_rev')
    elif computer_choice == 'scissors':
        computer_hand.configure_img('scissors_hand_rev')

    # winner of round is determined
    if your_choice == computer_choice:  # checks for tie
        round_text += "It's a tie!\n"
    elif your_choice == 'paper':
        if computer_choice == 'rock':  # paper covers rock
            round_text += "Paper covers rock, you win!\n"
            rounds_won += 1
        else:
            round_text += "Scissors cuts paper, you lose!\n"
            rounds_lost += 1
    elif your_choice == 'rock':
        if computer_choice == 'scissors':  # rock beats scissors
            round_text += "Rock beats scissors, you win!\n"
            rounds_won += 1
        else:
            round_text += "Paper covers rock, you lose!\n"
            rounds_lost += 1
    elif your_choice == 'scissors':
        if computer_choice == 'paper':  # scissors cuts paper
            round_text += "Scissors cuts paper, you win!\n"
            rounds_won += 1
        else:
            round_text += "Rock beats scissors, you lose!\n"
            rounds_lost += 1
    rounds_remaining -= 1

    # display scores on scoreboard
    your_score.configure(text=f"You: {rounds_won}                                ")
    computer_score.configure(text=f"Computer: {rounds_lost}")

    # to run when game ends
    if rounds_remaining == 0 or (rounds_lost > tr // 2) or (rounds_won > tr // 2):
        rounds_remaining = 0
        start_button.configure(fg=BLACK)
        if rounds_lost > rounds_won:  # if the user loses the game...
            if mode == 'easy':
                win_or_lose.configure(text="\nLOSE\nOh well, maybe you'll win next time...", fg=RED)
            else:
                win_or_lose.configure(text="\nLOSE\nIt's mine, all mine! You shall never win again...", fg=RED)
        elif rounds_lost < rounds_won:  # if the user wins the game...
            win_or_lose.configure(text="\nWIN\nYou emerged victorious! Well done...", fg=GREEN)
            if 'earn_points' in user.permissions:
              user.points += 20
              user.progress += 20
        else:  # if the game ends in a tie...
            win_or_lose.configure(text="\nTIE\nLooks like this game went nowhere...", fg=WHITE)
        rounds_won, rounds_lost = 0, 0  # reset

    round_info.configure(text=round_text)  # displays final text in app


# function for user to submit desired number of rounds and game mode, then start a new game
def start_game(user, rounds, mode):
    global total_rounds
    global rounds_remaining
    global game_mode
    # gets round number from rounds dropdown
    total_rounds = rounds.get()
    rounds_remaining = total_rounds
    # gets game mode from modes dropdown
    game_mode = mode.get()
    if game_mode == "medium" and repr(user) == "verified":
      if user.points < 10: # if the user can't afford medium mode (10p)
        print("You don't have enough points")
        return # end
      else:
        user.points -= 10
    # just in case someone changes their mind...
    global rounds_won
    global rounds_lost
    rounds_won, rounds_lost = 0, 0
    # changes to text
    round_info.configure(text="\nLet the game begin! \nPress either of the buttons above to play a round")
    win_or_lose.configure(text="")  
    your_hand.label.configure(image=None)
    computer_hand.label.configure(image=None) # because it's a new game

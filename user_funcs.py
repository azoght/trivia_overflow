'''
Functions that help the user navigate the application, including the many pages in this application
'''

from constants import *
from crypt_funcs import *
from classes.user_classes import * 
from classes.trivia_classes import *
from test_users import *
from posts_responses import *
from mod_user_funcs import *
from other_funcs import *

from tkinter import *
import time  # for dates

# additional componnent imports
from games.rps import *
from games.rpg import *
from games.quiz import *

def login(win, widgets): # logs in user
  # get user input
  username = widgets['username_entry'].get()
  password = widgets['password_entry'].get()

  # check user input
  if username in all_usernames: # if username exists...
    if username in test_admins.keys(): # if user is admin...
      if decrypt_password(test_admins[username]['password']) != password: # password is encrypted in text
        widgets['message'].configure(text="\nWrong password, try again!\n", fg='red')
      else:
        user = Admin(username, password, posts_responded_to=test_admins[username]['posts_responded_to'], posts_rewarded_for=test_admins[username]['posts_rewarded_for'], points=test_admins[username]['points'])
        adminoptions_page(win, widgets, user) # takes admin to options page
    elif username in test_verified.keys(): # if user is verified...
      if decrypt_password(test_verified[username]['password']) != password:
        widgets['message'].configure(text="\nWrong password, try again!\n", fg='red')
      else:
        user = Verified(username, password, posts_responded_to=test_verified[username]['posts_responded_to'], posts_rewarded_for=test_verified[username]['posts_rewarded_for'], points=test_verified[username]['points'])
        posts_page(win, widgets, user) # takes user to verified posts
  else:
    widgets['message'].configure(text="\nThis username doesn't exist!\n", fg='red') # changes text

def logout(win, widgets, user): # logs the user out and saves their information
  if repr(user) == "admin": # if user is admin...
    test_admins[user.name]['posts_reponded_to'] = user.posts_responded_to
    test_admins[user.name]['posts_rewarded_for'] = user.posts_rewarded_for
  elif repr(user) == "verified": # if the user is verified...
    test_verified[user.name]['posts_reponded_to'] = user.posts_responded_to
    test_verified[user.name]['posts_rewarded_for'] = user.posts_rewarded_for

def sign_up(win, widgets): # creates new account
  # get user input
  username = widgets['username_entry'].get()
  password = widgets['password_entry'].get()
  confirm = widgets['confirm_entry'].get()

  # sign user up
  if username in all_usernames: # if username exists...
    widgets['message'].configure(text="\nThis username is already taken!\n", fg='red')
  else:
    if len(password) < 8: # 8 characters is a standard minimum
      widgets['message'].configure(text="\nPassword too short, must be 8 characters or more!\n", fg='red')
    elif password == confirm: # if both passwords match...
      all_usernames.append(username)
      
      # create new user (starts as verified)
      test_verified[username] = {}

      test_verified[username]['password'] = encrypt_password(password)
      test_verified[username]['points'] = 0
      test_verified[username]['posts_responded_to'] = []
      test_verified[username]['posts_rewarded_for'] = []

      user = Verified(username, password)

      # take user to latest posts
      posts_page(win, widgets, user)

def return_from_posts(win, widgets, user): # returns user to previous page from posts
  if repr(user) == "admin": # if user is admin
    adminoptions_page(win, widgets, user)
  else:
    logout(win, widgets, user)
    home_page(win, widgets)

def submit_response(win, widgets, post, user, selected_option): # submits the set answer as a response
  answer = selected_option.get()
  if len(answer) >= 1:
    ans_letter = answer[0]
    your_response = Response(author_name=user.name, answer=ans_letter, date_posted=time.strftime("%m/%d/%Y")) # ex. January 1, 1970 is displayed as 01/01/1970
    post.responses = post.responses[::-1] # reverses the responses so that they are from oldest to latest; that way, the user's response will easily be added to it
    post.responses.append(your_response)
    post.responses = post.responses[::-1] # finally, we reverse it again, back to normal
    
    user.posts_responded_to.append(post.id_)

    post_page(win, widgets, user, post) # takes user back to post page

def post_question(win, widgets, user, correct_letter): # posts a question created by an admin
  global test_posts
  question_title = widgets['question_title_entry'].get()
  a_answer = widgets['option_a_entry'].get()
  b_answer = widgets['option_b_entry'].get()
  c_answer = widgets['option_c_entry'].get()
  d_answer = widgets['option_d_entry'].get()
  answers = [a_answer, b_answer, c_answer, d_answer]
  correct_answer = answers[['A','B','C','D'].index(correct_letter.get())]
  points = int(widgets['point_value_entry'].get())
  quota = int(widgets['quota_entry'].get())
  

  post = create_post_from_question(question_title, answers, correct_answer, points, user.name, time.strftime("%m/%d/%Y"), quota)

  test_posts = test_posts[::-1]
  test_posts.append(post)
  test_posts = test_posts[::-1]

  posts_page(win, widgets, user)

def reward_response(user, post): # rewards the user points based on whether or not they got a question correct
  if (len(post.responses) >= post.quota) and (post.id_ in user.posts_responded_to) and (post.id_ not in user.posts_rewarded_for) and ('earn_points' in user.permissions): 
      user.posts_rewarded_for.append(post.id_)
      ans_letter = find_user_response_in_post(user.name, post).answer
      if ['A', 'B', 'C', 'D'].index(ans_letter) == post.question.answers.index(post.question.correct_answer): # if user got correct answer
        print(f"Congratulations, {user.name}! You've just been awarded {post.question.point_value} points!")
        user.points += post.question.point_value
        user.progress += post.question.point_value
      else:
        print("Oof, you got the question wrong!")
        print(f"The correct answer was {['A', 'B', 'C', 'D'][post.question.answers.index(post.question.correct_answer)]}. {post.question.correct_answer}")
        print("Better luck next time!")
      print(f"You have {user.points} points!")
      user.posts_rewarded_for.append(post.id_)

def reward_question(creator, post): # rewards the admin who created a question points based on how much of the quota got the question right
  if (len(post.responses) >= post.quota) and (post.id_ not in creator.posts_rewarded_for) and ('earn_points' in creator.permissions):
    correct_answers = 0 # the number of correct answers found
    
    for response in post.responses[::-1][:post.quota]: # only checks the responses up until the post's quota was passed
      if ['A', 'B', 'C', 'D'].index(response.answer) == post.question.answers.index(post.question.correct_answer): # points awarded is based on the proportion of correct responses to the first responses before quota
        correct_answers += 1
    
    print(f"Based on users' correct responses, you've just been awarded {int(100 * correct_answers / post.quota)} points!")
    creator.points += int(100 * correct_answers / post.quota)
    creator.posts_rewarded_for.append(post.id_)
    print(f"You have {creator.points} points!")

def borrow_question(win, widgets, user):
  global test_posts
  if user.points < 10:
    print("User doesn't have enough points")
    return
  user.points -= 10  # it costs 10 points

  faucet = Trivia_Faucet(1)
  question = faucet.questions[0]
  
  quota = random.randint(1,10) # quota is random (for no reason)

  post = create_post_from_question(question.header, question.answers, question.correct_answer, question.point_value, user.name, time.strftime("%m/%d/%Y"), quota) # create post

  # add post
  test_posts = test_posts[::-1] # reverses list
  test_posts.append(post)
  test_posts = test_posts[::-1] # reverses list

  posts_page(win, widgets, user)

# pages!

def page_transition(widgets):
  for widget in widgets.values():
    widget.destroy() # deletes the widget
  widgets = dict()
  return widgets # returns as an empty dict

##home page
def home_page(win, widgets):
  widgets = page_transition(widgets)

  # frames
  widgets['main_frame'] = Frame(win, bg=BG_COLOR)
  widgets['main_frame'].place(x=WIDTH/2, y=HEIGHT/2, anchor='c')

  # buttons and spacers
  widgets['login_button'] = Button(widgets['main_frame'], text="Login", width=15, height=2, bd=0, command=lambda:login_page(win, widgets))
  widgets['login_button'].pack()

  widgets['spacer_1'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_1'].pack()

  widgets['signup_button'] = Button(widgets['main_frame'], text="Sign Up", width=15, height=2, bd=0, command=lambda:signup_page(win, widgets))
  widgets['signup_button'].pack()

  widgets['spacer_2'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_2'].pack()

  widgets['continue_button'] = Button(widgets['main_frame'], text="Continue as Guest", width=15, height=2, bd=0, command=lambda:posts_page(win, widgets, Guest()))
  widgets['continue_button'].pack()

##login page
def login_page(win, widgets):
  widgets = page_transition(widgets)

  # frames and spacers
  widgets['main_frame'] = Frame(win, bg=BG_COLOR)
  widgets['main_frame'].place(x=WIDTH/2, y=HEIGHT/2, anchor='c')

  widgets['username_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)
  widgets['username_frame'].pack()

  widgets['spacer_1'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_1'].pack()

  widgets['password_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)
  widgets['password_frame'].pack()

  widgets['spacer_2'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_2'].pack()

  # username frame componnents
  widgets['username_label'] = Label(widgets['username_frame'], text='Username: ', bg=BG_COLOR)
  widgets['username_label'].pack(side=LEFT)

  widgets['username_entry'] = Entry(widgets['username_frame'], width=15)
  widgets['username_entry'].pack(side=RIGHT)

  # password frame componnents
  widgets['password_label'] = Label(widgets['password_frame'], text='Password: ', bg=BG_COLOR)
  widgets['password_label'].pack(side=LEFT)

  widgets['password_entry'] = Entry(widgets['password_frame'], width=15, show='*') # password entered displayed as '*'
  widgets['password_entry'].pack(side=RIGHT)

  # buttons and message
  widgets['login_button'] = Button(widgets['main_frame'], text="Log In", width=15, height=2, bd=0, command=lambda:login(win, widgets))
  widgets['login_button'].pack()

  widgets['message'] = Label(widgets['main_frame'], text="\n\n", bg=BG_COLOR)
  widgets['message'].pack()

  widgets['return_button'] = Button(widgets['main_frame'], text="Go Back", width=15, height=2, bd=0, command=lambda:home_page(win, widgets))
  widgets['return_button'].pack(side=BOTTOM)

##sign up page
def signup_page(win, widgets):
  page_transition(widgets)

  # frames and spacers
  widgets['main_frame'] = Frame(win, bg=BG_COLOR)
  widgets['main_frame'].place(x=WIDTH/2, y=HEIGHT/1.8, anchor='c')

  widgets['username_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)
  widgets['username_frame'].pack()

  widgets['spacer_1'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_1'].pack()

  widgets['password_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)
  widgets['password_frame'].pack()

  widgets['spacer_2'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_2'].pack()

  widgets['confirm_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)
  widgets['confirm_frame'].pack()

  widgets['spacer_3'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_3'].pack()

  # username frame componnents
  widgets['username_label'] = Label(widgets['username_frame'], text='Username: ', bg=BG_COLOR)
  widgets['username_label'].pack(side=LEFT)

  widgets['username_entry'] = Entry(widgets['username_frame'], width=15)
  widgets['username_entry'].pack(side=RIGHT)
  
  # password frame componnents
  widgets['password_label'] = Label(widgets['password_frame'], text='Password: ', bg=BG_COLOR)
  widgets['password_label'].pack(side=LEFT)

  widgets['password_entry'] = Entry(widgets['password_frame'], width=15, show='*') 
  widgets['password_entry'].pack(side=RIGHT)
  
  # confirm password frame componnents
  widgets['confirm_label'] = Label(widgets['confirm_frame'], text='Confirm Password: ', bg=BG_COLOR)
  widgets['confirm_label'].pack(side=LEFT)

  widgets['confirm_entry'] = Entry(widgets['confirm_frame'], width=15, show='*') # password entered displayed as '*'
  widgets['confirm_entry'].pack(side=RIGHT)
  
  # buttons and message
  widgets['create_account_button'] = Button(widgets['main_frame'], text="Create Account", width=15, height=2, bd=0, command=lambda:sign_up(win, widgets))
  widgets['create_account_button'].pack()

  widgets['message'] = Label(widgets['main_frame'], text="\n\n", bg=BG_COLOR)
  widgets['message'].pack()

  widgets['return_button'] = Button(widgets['main_frame'], text="Go Back", width=15, height=2, bd=0, command=lambda:home_page(win, widgets))
  widgets['return_button'].pack(side=BOTTOM)

##latest posts page
def posts_page(win, widgets, user, page=1):
  widgets = page_transition(widgets)

  # frames 
  widgets['post_frame'] = Frame(win, bg=BG_COLOR)
  widgets['post_frame'].pack(side=LEFT)

  widgets['bottom_frame_1'] = Frame(win, bg=BG_COLOR)
  widgets['bottom_frame_1'].place(x=320, y=350) # at (320, 350)

  widgets['bottom_frame_2'] = Frame(win, bg=BG_COLOR)
  widgets['bottom_frame_2'].place(x=650, y=350)

  # posts in post frame (4 at a time)

  post_index = 4*(page-1) # the index of the post in the posts list

  total_pages = round((len(test_posts) + 1) / 4) # depends on length of post list

  # first post
  post_text = f"{condense(test_posts[post_index].question.header)} [{test_posts[post_index].question.point_value}]\nBy {test_posts[post_index].author_name} on {test_posts[post_index].date_posted}"
  widgets['post_button_1'] = Button(widgets['post_frame'], text=post_text, anchor='w', bd=0, bg=BG_COLOR, command=lambda:post_page(win, widgets, user, get_post(widgets['post_button_1']['text'], test_posts)))
  widgets['post_button_1'].pack(fill='both')
  widgets['spacer_1'] = Label(widgets['post_frame'], text='', bg=BG_COLOR, font=('Helvetica', 2))
  widgets['spacer_1'].pack()

  # second post
  post_index += 1
  if len(test_posts) > post_index: # checks if previously displayed post is oldest
    post_text = f"{condense(test_posts[post_index].question.header)} [{test_posts[post_index].question.point_value}]\nBy {test_posts[post_index].author_name} on {test_posts[post_index].date_posted}"
    widgets['post_button_2'] = Button(widgets['post_frame'], text=post_text, anchor='w', bd=0, bg=BG_COLOR, command=lambda:post_page(win, widgets, user, get_post(widgets['post_button_2']['text'], test_posts)))
    widgets['post_button_2'].pack(fill='both')
    widgets['spacer_2'] = Label(widgets['post_frame'], text='', bg=BG_COLOR, font=('Helvetica', 2))
    widgets['spacer_2'].pack()

  # third post
  post_index += 1
  if len(test_posts) > post_index: 
    post_text = f"{condense(test_posts[post_index].question.header)} [{test_posts[post_index].question.point_value}]\nBy {test_posts[post_index].author_name} on {test_posts[post_index].date_posted}"
    widgets['post_button_3'] = Button(widgets['post_frame'], text=post_text, anchor='w', bd=0, bg=BG_COLOR, command=lambda:post_page(win, widgets, user, get_post(widgets['post_button_3']['text'], test_posts)))
    widgets['post_button_3'].pack(fill='both')
    widgets['spacer_3'] = Label(widgets['post_frame'], text='', bg=BG_COLOR, font=('Helvetica', 2))
    widgets['spacer_3'].pack()

  # fourth post
  post_index += 1
  if len(test_posts) > post_index:
    post_text = f"{condense(test_posts[post_index].question.header)} [{test_posts[post_index].question.point_value}]\nBy {test_posts[post_index].author_name} on {test_posts[post_index].date_posted}"
    widgets['post_button_4'] = Button(widgets['post_frame'], text=post_text, anchor='w', bd=0, bg=BG_COLOR, command=lambda:post_page(win, widgets, user, get_post(widgets['post_button_4']['text'], test_posts)))
    widgets['post_button_4'].pack(fill='both')
    widgets['spacer_4'] = Label(widgets['post_frame'], text='', bg=BG_COLOR, font=('Helvetica', 2))
    widgets['spacer_4'].pack()

  # games button
  widgets['games_button'] = Button(win, text='Games', bg='magenta', width=5, height=1, bd=0, command=lambda:games_page(win, widgets, user))
  widgets['games_button'].place(x=50, y=350) # at (50, 350)

  # bottom frame componnents
  if page > 1:
    widgets['prev_button'] = Button(widgets['bottom_frame_1'], text='<', width=2, height=1, bd=0, anchor='c', command=lambda:posts_page(win, widgets, user, page=page-1))
    widgets['prev_button'].pack(side=LEFT)
  widgets['page_num_label'] = Label(widgets['bottom_frame_1'], text=' '*6 + f"Page {page} of {total_pages}" + ' '*6, anchor='c', bg=BG_COLOR)
  widgets['page_num_label'].pack(side=LEFT)
  if page < total_pages: # if we've haven't reached the end...
    widgets['next_button'] = Button(widgets['bottom_frame_1'], text='>', width=2, height=1, bd=0, anchor='c', command=lambda:posts_page(win, widgets, user, page=page+1)) # takes user to next page
    widgets['next_button'].pack(side=LEFT)

  # return button
  widgets['return_button'] = Button(widgets['bottom_frame_2'], text="Return", width=5, height=1, bd=0, command=lambda:return_from_posts(win, widgets, user))
  widgets['return_button'].grid(row=0, column=3)

  # create question button (visible only if user is Admin)
  if repr(user) == "admin":
    widgets['plus_button'] = Button(widgets['bottom_frame_2'], text="+", width=2, height=1, bd=0, command=lambda:createquestion_page(win, widgets, user))
    widgets['plus_button'].grid(row=0, column=0)

    widgets['button_spacer'] = Label(widgets['bottom_frame_2'], text="  ", bg=BG_COLOR)
    widgets['button_spacer'].grid(row=0, column=1)

##post page
def post_page(win, widgets, user, post):

  if post.author_name == user.name: # if user created this post
    reward_question(user, post)
  else:
    reward_response(user, post)
  
  widgets = page_transition(widgets)

  # frames
  widgets['main_frame'] = Frame(win, bg=BG_COLOR)
  widgets['main_frame'].place(y=70)

  widgets['button_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)

  # text and buttons
  widgets['question_description'] = Text(widgets['main_frame'], bg=BG_COLOR, bd=0, width=100, height=8, font=('Helvetica',10))
  widgets['question_description'].insert(INSERT, f"{post.question.header} [{post.question.point_value}]\nBy {post.author_name} on {post.date_posted}\n\nA. {post.question.answers[0]}\nB. {post.question.answers[1]}\nC. {post.question.answers[2]}\nD. {post.question.answers[3]}")
  widgets['question_description'].configure(state='disabled') # makes text read-only
  widgets['question_description'].pack()

  widgets['button_frame'].pack()

  if repr(user) != "guest" and user.name != post.author_name: # if the user is not a guest and didn't create the post
    if (repr(user) == "verified" or repr(user) == "admin") and (post.id_ not in user.posts_responded_to): # if they didn't already respond
      widgets['respond_button'] = Button(widgets['button_frame'], text="Respond", width=5, height=1, bd=0, command=lambda:createresponse_page(win, widgets, user, post))
      widgets['respond_button'].pack(side=LEFT)

  widgets['return_button'] = Button(widgets['button_frame'], text="Return", width=5, height=0, bd=0, command=lambda:posts_page(win, widgets, user, page=(test_posts.index(post) // 4) + 1))
  widgets['return_button'].pack(side=LEFT)

  ##responses
  widgets['responses'] = Text(widgets['main_frame'], bg=BG_COLOR, bd=0, width=100, height=7, font=('Helvetica', 10))
  widgets['responses'].insert(INSERT, f"Responses ({len(post.responses)})\n") # only two latest responses displayed

  if len(post.responses) >= 1:
    widgets['responses'].insert(END, f"\n{post.responses[0].author_name} on {post.responses[0].date_posted}\n{post.responses[0].answer}\n") # adds latest response

  if len(post.responses) >= 2:
    widgets['responses'].insert(END, f"\n{post.responses[1].author_name} on {post.responses[1].date_posted}\n{post.responses[1].answer}\n") # adds second latest response

  widgets['responses'].configure(state='disabled')
  widgets['responses'].pack()

##create response page
def createresponse_page(win, widgets, user, post):
  widgets = page_transition(widgets)

  # frames
  widgets['main_frame'] = Frame(win, bg=BG_COLOR)
  widgets['main_frame'].pack(side=LEFT)

  widgets['button_frame'] = Frame(win, bg=BG_COLOR)

  # other componnents
  widgets['question_description'] = Text(widgets['main_frame'], bg=BG_COLOR, bd=0, width=100, height=5, font=('Helvetica', 10))
  widgets['question_description'].insert(INSERT, f"Question Title: {post.question.header}\nPoint Value: {post.question.point_value}\nWhat do you think the answer is?\n")
  widgets['question_description'].configure(state='disabled')
  widgets['question_description'].pack()

  # dropdown menu to select answer
  options = [f"A. {post.question.answers[0]}", f"B. {post.question.answers[1]}", f"C. {post.question.answers[2]}", f"D. {post.question.answers[3]}"]
  selected_option = StringVar(widgets['main_frame']) # keeps track of dropdown selection
  select_answer = OptionMenu(widgets['main_frame'], selected_option, *options)
  select_answer.pack()

  # button frame componnents
  widgets['submit_button'] = Button(widgets['button_frame'], text="Submit", width=5, height=1, bd=0, command=lambda:submit_response(win, widgets, post, user, selected_option))
  widgets['submit_button'].pack(side=LEFT)

  widgets['button_spacer'] = Label(widgets['button_frame'], text='  ', bg=BG_COLOR)
  widgets['button_spacer'].pack(side=LEFT)

  widgets['cancel_button'] = Button(widgets['button_frame'], text="Cancel", width=5, height=1, bd=0, command=lambda:post_page(win, widgets, user, post))
  widgets['cancel_button'].pack(side=LEFT)

  widgets['button_frame'].place(x=WIDTH/2, y=HEIGHT*0.75, anchor='c')

##admin options page
def adminoptions_page(win, widgets, admin):
  widgets = page_transition(widgets)

  # frames
  widgets['main_frame'] = Frame(win, bg=BG_COLOR)
  widgets['main_frame'].place(x=WIDTH/2, y=HEIGHT/2, anchor='c')

  # message, spacers, and buttons
  widgets['welcome_msg'] = Label(widgets['main_frame'], text=f"\nWelcome, {admin.name}!\n", anchor='c', bg=BG_COLOR)
  widgets['welcome_msg'].pack()

  widgets['modify_button'] = Button(widgets['main_frame'], text="Modify Users", width=15, height=2, bd=0, command=lambda:modifyusers_page(win, widgets, admin))
  widgets['modify_button'].pack()

  widgets['spacer_1'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_1'].pack()

  widgets['posts_button'] = Button(widgets['main_frame'], text="Go To Posts", width=15, height=2, bd=0, command=lambda:posts_page(win, widgets, admin))
  widgets['posts_button'].pack()

  widgets['spacer_2'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_2'].pack()

  widgets['logout_button'] = Button(widgets['main_frame'], text="Log Out", width=15, height=2, bd=0, command=lambda:home_page(win, widgets))
  widgets['logout_button'].pack()

##create question page
def createquestion_page(win, widgets, user):
  widgets = page_transition(widgets)

  # frames
  widgets['main_frame'] = Frame(win, bg=BG_COLOR)
  widgets['main_frame'].place(y=220, anchor='w')

  widgets['question_title_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)

  ##option frames
  widgets['option_a_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)
  widgets['option_b_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)
  widgets['option_c_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)
  widgets['option_d_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)

  widgets['correct_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)
  
  widgets['point_value_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)
  widgets['quota_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)

  widgets['buttons_frame'] = Frame(win, bg=BG_COLOR)

  # question title frame componnents
  widgets['question_title_label'] = Text(widgets['question_title_frame'], bg=BG_COLOR, bd=0, width=len("Question Title: "), height=1, font=('Helvetica', 10))
  widgets['question_title_label'].insert(INSERT, "Question Title: ")
  widgets['question_title_label'].configure(state='disabled')
  widgets['question_title_label'].grid(row=0, column=0)

  widgets['question_title_entry'] = Entry(widgets['question_title_frame'], width=100)
  widgets['question_title_entry'].grid(row=0, column=1)

  widgets['question_title_frame'].grid(row=0)

  widgets['options_label'] = Text(widgets['main_frame'], bg=BG_COLOR, bd=0, width=117, height=1, font=('Helvetica', 10))
  widgets['options_label'].insert(INSERT, "Options: ")
  widgets['options_label'].configure(state='disabled')
  widgets['options_label'].grid(row=1)

  # option a frame componnents
  widgets['option_a_label'] = Text(widgets['option_a_frame'], bg=BG_COLOR, bd=0, width=10, height=1, font=('Helvetica', 10))
  widgets['option_a_label'].insert(INSERT, "A. ")
  widgets['option_a_label'].configure(state='disabled')
  widgets['option_a_label'].grid(row=0,column=0)

  widgets['option_a_entry'] = Entry(widgets['option_a_frame'], width=100, bd=0, font=('Helvetica', 10))
  widgets['option_a_entry'].grid(row=0, column=1)

  widgets['option_a_frame'].grid(row=2)

  # option b frame componnents
  widgets['option_b_label'] = Text(widgets['option_b_frame'], bg=BG_COLOR, bd=0, width=10, height=1, font=('Helvetica', 10))
  widgets['option_b_label'].insert(INSERT, "B. ")
  widgets['option_b_label'].configure(state='disabled')
  widgets['option_b_label'].grid(row=0, column=0)

  widgets['option_b_entry'] = Entry(widgets['option_b_frame'], width=100, bd=0, font=('Helvetica', 10))
  widgets['option_b_entry'].grid(row=0, column=1)

  widgets['option_b_frame'].grid(row=3)

  # option c frame componnents
  widgets['option_c_label'] = Text(widgets['option_c_frame'], bg=BG_COLOR, bd=0, width=10, height=1, font=('Helvetica', 10))
  widgets['option_c_label'].insert(INSERT, "C. ")
  widgets['option_c_label'].configure(state='disabled')
  widgets['option_c_label'].grid(row=0, column=0)

  widgets['option_c_entry'] = Entry(widgets['option_c_frame'], width=100, bd=0, font=('Helvetica', 10))
  widgets['option_c_entry'].grid(row=0, column=1)

  widgets['option_c_frame'].grid(row=4)

  # option d frame componnents
  widgets['option_d_label'] = Text(widgets['option_d_frame'], bg=BG_COLOR, bd=0, width=10, height=1, font=('Helvetica', 10))
  widgets['option_d_label'].insert(INSERT, "D. ")
  widgets['option_d_label'].configure(state='disabled')
  widgets['option_d_label'].grid(row=0, column=0)

  widgets['option_d_entry'] = Entry(widgets['option_d_frame'], width=100, bd=0, font=('Helvetica', 10))
  widgets['option_d_entry'].grid(row=0, column=1)

  widgets['option_d_frame'].grid(row=5)

  # correct answer frame componnents
  widgets['correct_answer_label'] = Text(widgets['correct_frame'], bg=BG_COLOR, bd=0, width=20, height=1, font=('Helvetica', 10))
  widgets['correct_answer_label'].insert(INSERT, "Correct Answer: ")
  widgets['correct_answer_label'].configure(state='disabled')
  widgets['correct_answer_label'].grid(row=0, column=0)

  correct_ans_letter = StringVar(widgets['correct_frame'])
  widgets['correct_select'] = OptionMenu(widgets['correct_frame'], correct_ans_letter, *['A', 'B', 'C', 'D'])
  widgets['correct_select'].config(width=92)
  widgets['correct_select'].grid(row=0, column=1)

  widgets['correct_frame'].grid(row=6)

  # point value frame componnents
  widgets['point_value_label'] = Text(widgets['point_value_frame'], bg=BG_COLOR, bd=0, width=len("Point Value: "), height=1, font=('Helvetica', 10))
  widgets['point_value_label'].insert(INSERT, "Point Value: ")
  widgets['point_value_label'].configure(state='disabled')
  widgets['point_value_label'].grid(row=0, column=0)

  widgets['point_value_entry'] = Entry(widgets['point_value_frame'], width=104, bd=0, font=('Helvetica', 10))
  widgets['point_value_entry'].grid(row=0, column=1)

  widgets['point_value_frame'].grid(row=7)

  # quota frame componnents
  widgets['quota_label'] = Text(widgets['quota_frame'], bg=BG_COLOR, bd=0, width=len("Quota (maximum responses before points rewarded): "), height=1, font=('Helvetica', 10))
  widgets['quota_label'].insert(INSERT, "Quota (maximum responses before points rewarded): ")
  widgets['quota_label'].configure(state='disabled')
  widgets['quota_label'].grid(row=0, column=0)

  widgets['quota_entry'] = Entry(widgets['quota_frame'], width=67, bd=0, font=('Helvetica', 10))
  widgets['quota_entry'].grid(row=0, column=1)

  widgets['quota_frame'].grid(row=8)

  widgets['vertical_spacer'] = Label(widgets['main_frame'], bg=BG_COLOR, text="\n\n")
  widgets['vertical_spacer'].grid(row=9)

  # buttons frame componnents
  widgets['post_button'] = Button(widgets['buttons_frame'], text="Post", width=5, height=1, bd=0, command=lambda:post_question(win, widgets, user, correct_ans_letter))
  widgets['post_button'].grid(row=0, column=0)

  widgets['horizontal_spacer_1'] = Label(widgets['buttons_frame'], text="    ", bg=BG_COLOR)
  widgets['horizontal_spacer_1'].grid(row=0, column=1)

  widgets['borrow_button'] = Button(widgets['buttons_frame'], text="Borrow from OpenTrivia (10 p)", width=25, height=1, bd=0, command=lambda:borrow_question(win, widgets, user))
  widgets['borrow_button'].grid(row=0, column=2)

  widgets['horizontal_spacer_2'] = Label(widgets['buttons_frame'], text="    ", bg=BG_COLOR)
  widgets['horizontal_spacer_2'].grid(row=0, column=3)

  widgets['cancel_button'] = Button(widgets['buttons_frame'], text="Cancel", width=10, height=1, bd=0, command=lambda:posts_page(win, widgets, user))
  widgets['cancel_button'].grid(row=0, column=4)

  widgets['buttons_frame'].pack(side=BOTTOM)

##modify users options page
def modifyusers_page(win, widgets, admin):
  widgets = page_transition(widgets)

   # frames
  widgets['main_frame'] = Frame(win, bg=BG_COLOR)
  widgets['main_frame'].place(x=WIDTH/2, y=HEIGHT/2, anchor='c')

  # spacers and buttons

  widgets['delete_user_button'] = Button(widgets['main_frame'], text="Delete User", width=15, height=2, bd=0, command=lambda:deleteuser_page(win, widgets, admin))
  widgets['delete_user_button'].pack()

  widgets['spacer_1'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_1'].pack()

  widgets['promote_user_button'] = Button(widgets['main_frame'], text="Promote User To Admin", width=15, height=2, bd=0, command=lambda:promoteuser_page(win, widgets, admin))
  widgets['promote_user_button'].pack()

  widgets['spacer_2'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_2'].pack()

  widgets['return_button'] = Button(widgets['main_frame'], text="Return", width=15, height=2, bd=0, command=lambda:adminoptions_page(win, widgets, admin))
  widgets['return_button'].pack()

##delete user page
def deleteuser_page(win, widgets, admin, page=1):
  start_index = 5 * (page-1)

  qualified_users = filter(lambda x: (Verified(x, test_verified[x]['password'], points=test_verified[x]['points']).get_level() >= 10), list(test_verified.keys())) # only verified users of level 10 or above are qualified to become admins

  qualified_users = list(qualified_users)

  if page < 1 or start_index > len(qualified_users): # if we're out of bounds...
    return  # ...do nothing
  
  widgets = page_transition(widgets)

  # frames 
  widgets['main_frame'] = Frame(win, bg=BG_COLOR)
  widgets['main_frame'].place(x=WIDTH/2, y=HEIGHT/2, anchor='c')

  widgets['users_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)

  widgets['buttons_frame'] = Frame(win, bg=BG_COLOR)

  # text 
  widgets['click_username'] = Label(widgets['main_frame'], text="Click a user's name to delete them\n", bg=BG_COLOR)
  widgets['click_username'].pack()

  # users frame componnents
  start_index = 5 * (page-1)

  if len(test_verified.keys()) - start_index < 5:
    end_index = len(test_verified.keys())
  else:
    end_index = start_index + 5
  
  usernames = list(test_verified.keys())[start_index:end_index]

  i = 0

  widgets['username_button_1'] = Button(widgets['users_frame'], text=usernames[0], width=len(usernames[0]), height=1, bg=BG_COLOR, command=lambda:delete_user(usernames[0]))
  widgets['username_button_1'].pack()

  i += 1

  if i != len(usernames):
    widgets['username_button_2'] = Button(widgets['users_frame'], text=usernames[1], width=len(usernames[1]), height=1, bg=BG_COLOR, command=lambda:delete_user(usernames[1]))
    widgets['username_button_2'].pack()

  i += 1

  if i != len(usernames):
    widgets['username_button_3'] = Button(widgets['users_frame'], text=usernames[2], width=len(usernames[2]), height=1, bg=BG_COLOR, command=lambda:delete_user(usernames[2]))
    widgets['username_button_3'].pack()

  i += 1

  if i != len(usernames):
    widgets['username_button_4'] = Button(widgets['users_frame'], text=usernames[3], width=len(usernames[3]), height=1, bg=BG_COLOR, command=lambda:delete_user(usernames[3]))
    widgets['username_button_4'].pack()

  i += 1

  if i != len(usernames):
    widgets['username_button_5'] = Button(widgets['users_frame'], text=usernames[4], width=len(usernames[4]), height=1, bg=BG_COLOR, command=lambda:delete_user(usernames[4]))
    widgets['username_button_5'].pack()

  widgets['users_frame'].pack()

  # buttons frame componnents
  widgets['prev_page_button'] = Button(widgets['buttons_frame'], text="Previous Page", width=15, height=3, command=lambda:deleteuser_page(win, widgets, admin, page=page-1))
  widgets['prev_page_button'].pack(side=LEFT)

  widgets['next_page_button'] = Button(widgets['buttons_frame'], text="Next Page", width=15, height=3, command=lambda:deleteuser_page(win, widgets, admin, page=page+1))
  widgets['next_page_button'].pack(side=LEFT)

  widgets['return_button'] = Button(widgets['buttons_frame'], text="Go Back", width=15, height=3, command=lambda:modifyusers_page(win, widgets, admin))
  widgets['return_button'].pack(side=LEFT)

  widgets['buttons_frame'].pack(side=BOTTOM)


##promote user to admin page
def promoteuser_page(win, widgets, admin, page=1):
  start_index = 5 * (page-1)

  qualified_users = filter(lambda x: (Verified(x, test_verified[x]['password'], points=test_verified[x]['points']).get_level() >= 10), list(test_verified.keys())) 

  qualified_users = list(qualified_users)

  if page < 1 or start_index > len(qualified_users): 
    return  
  
  widgets = page_transition(widgets)

  # frames 
  widgets['main_frame'] = Frame(win, bg=BG_COLOR)
  widgets['main_frame'].place(x=WIDTH/2, y=HEIGHT/2, anchor='c')

  widgets['users_frame'] = Frame(widgets['main_frame'], bg=BG_COLOR)

  widgets['buttons_frame'] = Frame(win, bg=BG_COLOR)

  # text
  widgets['click_username'] = Label(widgets['main_frame'], text="Click a user's name to promote them to admin\n", bg=BG_COLOR)
  widgets['click_username'].pack()

  # users frame componnents

  if len(qualified_users) - start_index < 5:
    end_index = len(qualified_users)
  else:
    end_index = start_index + 5
        
  usernames = qualified_users[start_index:end_index]

  for i, username in enumerate(usernames):
    widgets['username_button'+str(i+1)] = Button(widgets['users_frame'], text=username, width=len(username), height=1, bg=BG_COLOR, command=lambda:promote_user(username))
    widgets['username_button'+str(i+1)].pack()

  widgets['users_frame'].pack()

  # buttons frame componnents
  widgets['prev_page_button'] = Button(widgets['buttons_frame'], text="Previous Page", width=15, height=3, command=lambda:deleteuser_page(win, widgets, admin, page=page-1))
  widgets['prev_page_button'].pack(side=LEFT)

  widgets['next_page_button'] = Button(widgets['buttons_frame'], text="Next Page", width=15, height=3, command=lambda:deleteuser_page(win, widgets, admin, page=page+1))
  widgets['next_page_button'].pack(side=LEFT)

  widgets['return_button'] = Button(widgets['buttons_frame'], text="Go Back", width=15, height=3, command=lambda:modifyusers_page(win, widgets, admin))
  widgets['return_button'].pack(side=LEFT)

  widgets['buttons_frame'].pack(side=BOTTOM)

##games page
def games_page(win, widgets, user):
  widgets = page_transition(widgets)

  # frames
  widgets['main_frame'] = Frame(win, bg=BG_COLOR)
  widgets['main_frame'].place(x=WIDTH/2, y=HEIGHT/2, anchor='c')

  # buttons and spacers
  widgets['rps_button'] = Button(widgets['main_frame'], text="Rock, Paper, Scissors", width=20, height=2, bd=0, command=lambda:launch_rps(user))
  widgets['rps_button'].pack()

  widgets['spacer_1'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_1'].pack()

  widgets['rpg_button'] = Button(widgets['main_frame'], text="Creatures in Pythonia RPG", width=20, height=2, bd=0, command=lambda:launch_rpg())
  widgets['rpg_button'].pack()

  widgets['spacer_2'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_2'].pack()

  widgets['quiz_button'] = Button(widgets['main_frame'], text="Fun Form", width=20, height=2, bd=0, command=lambda:launch_quiz())
  widgets['quiz_button'].pack()

  widgets['spacer_3'] = Label(widgets['main_frame'], text='', bg=BG_COLOR)
  widgets['spacer_3'].pack()

  widgets['return_button'] = Button(widgets['main_frame'], text="Return", width=10, height=2, bd=0, command=lambda:posts_page(win, widgets, user))
  widgets['return_button'].pack()

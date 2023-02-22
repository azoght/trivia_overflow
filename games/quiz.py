"""
A GUI Buzzfeed-style quiz built using Tkinter where I use your preferences to determine what language you should be coding in
"""

from tkinter import * # for GUI

from PIL import Image, ImageTk # for images, pip install pillow first

import random


# fonts
helv18 = ('Helvetica', 18)

# global variables
global lang_points
global answer_list

lang_points = { # a dictionary representing the number of points for each category
    'python': 0,
    'java': 0,
    'rust': 0,
    'html': 0
}

answer_list = [None for _ in range(10)] # list of tuples representing languages behind answers + their questions' point value

# classes

class ScrollableFrame:
    """
    from https://stackoverflow.com/questions/1844995/how-to-add-a-scrollbar-to-a-window-with-tkinter
    by Kanwar Adnan
    creates a scrollbar within the main frame
    """
    def __init__ (self,master,width,height,mousescroll=0):
        self.mousescroll = mousescroll
        self.master = master
        self.height = height
        self.width = width
        self.main_frame = Frame(self.master)
        self.main_frame.pack(fill=BOTH,expand=1)

        self.scrollbar = Scrollbar(self.main_frame, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT,fill=Y)

        self.canvas = Canvas(self.main_frame,yscrollcommand=self.scrollbar.set)
        self.canvas.pack(expand=True,fill=BOTH)

        self.scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))

        self.frame = Frame(self.canvas,width=self.width,height=self.height)
        self.frame.pack(expand=True,fill=BOTH)
        self.canvas.create_window((0,0), window=self.frame, anchor="nw")

        self.frame.bind("<Enter>", self.entered)
        self.frame.bind("<Leave>", self.left)

    def _on_mouse_wheel(self,event):
        self.canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    def entered(self,event):
        if self.mousescroll:
            self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        
    def left(self,event):
        if self.mousescroll:
            self.canvas.unbind_all("<MouseWheel>")

class Question:

    def __init__(self, window, number, title, options, point_value):

        # to create space between questions
        s = (number-1)*100
        
        # question title
        self.title = Label(window, text=title, font=helv18)
        self.title.place(x=400, y=(number*200)-135+s, anchor='c')

        # options frame
        random.shuffle(options)
        self.q_frame = Frame(window, width=400, height=200)
        self.q_frame.place(x=400, y=(number*200)+s, anchor='c')

        ##first option (on top left)
        Button(self.q_frame, image=options[0].image, bd=0, command=lambda: answer(options[0].text.lower(), point_value, number)).grid(row=0, column=0)

        ##second option (on top right)
        Button(self.q_frame, image=options[1].image, bd=0, command=lambda: answer(options[1].text.lower(), point_value, number)).grid(row=0, column=1)

        ##third option (on bottom left)
        Button(self.q_frame, image=options[2].image, bd=0, command=lambda: answer(options[2].text.lower(), point_value, number)).grid(row=1, column=0)

        ##fourth option (on bottom right)
        Button(self.q_frame, image=options[3].image, bd=0, command=lambda: answer(options[3].text.lower(), point_value, number)).grid(row=1, column=1)

        # initialize point value...for now
        self.point_value = point_value

class Option:

    def __init__(self, text, filename):
        self.text = text
        self.image = ImageTk.PhotoImage(Image.open("images/" + filename).resize((300, 120))) # takes image from images folder and resizes it

def answer(answer, points, num):
    lang = ''
    if answer in ['what the hail?!', 'pythagoras', 'andrew garfield', 'pancakes', 'ukraine', 'lofi', 'slither.io', 'discord', 'derivatives', 'oliver twist']:
        lang = 'python'
    elif answer in ['i will send you to jesus...', 'plato', 'toby mcguire', 'eggs', 'spain', 'blues', 'among us', 'twitter', 'limits', 'great expectations']:
        lang = 'java'
    elif answer in ['e-motional da-mage!', 'socrates', 'tom holland', 'oatmeal', 'denmark', 'rock', 'animal crossing', 'reddit', 'integrals', 'bleak house']:
        lang = 'rust'
    elif answer in ['before physics was invented...', 'aristotle', 'peter parker', 'chocolate toast', 'vatican city', 'rap', 'skribbl.io', 'pinterest', 'graphing', 'a tale of two cities']:
        lang = 'html'
    answer_list[num-1] = (lang, points)

def finish_quiz():
    global lang_points
    if None not in answer_list:
        for answer in answer_list:
            lang_points[answer[0]] += answer[1]

        result = list(lang_points.keys())[list(lang_points.values()).index(max(list(lang_points.values())))]
        lang_points = {'python': 0, 'java': 0, 'rust': 0, 'html': 0} # clears dictionary
        go_to_result(result)

def go_to_result(res):
    # create new window
    result_page = Tk()
    result_page.title("Result")
    result_page.geometry("500x300")

    result_text = Text(result_page, font=('Helvetica', 16), wrap=WORD)

    # display text and logo based on result
    if res == 'python':
        result_text.insert(INSERT, "You got Python!")
        result_text.insert(INSERT, "\n\nCreated in 1991 by Guido Van Rossum, Python is a popular language known for its readability, simplicity, and fast execution. It is mostly used for machine learning, data science, applications, web development, and game development.")
        result_text.insert(INSERT, "\n\nLearn Python here at: https://www.w3schools.com/python/default.asp!")
    elif res == 'java':
        result_text.insert(INSERT, "You got Java!")
        result_text.insert(INSERT, "\n\nReleased in 1995 by James Gosling and Sun Microsystems, Java is a language known for its object oriented programming, security, and portability. It is used for applications, web servers, and management of big data.")
        result_text.insert(INSERT, "\n\nLearn Java here at: https://www.w3schools.com/java/default.asp!")
    elif res == 'rust':
        result_text.insert(INSERT, "You got Rust!")
        result_text.insert(INSERT, "\n\nDeveloped by Graydon Hoare in 2006 and now owned by Mozilla Labs, Rust is a systems-level language focused on security, speed, and concurrency. It is effective for creating operating systems, browser engines, online services, and embedded devices.")
        result_text.insert(INSERT, "\n\nLearn Rust here at: https://www.tutorialspoint.com/rust/index.htm!")
    elif res == 'html':
        result_text.insert(INSERT, "You got HTML!")
        result_text.insert(INSERT, "\n\nPublished in 1995 by by Berners-Lee, Hyper Text Markup Language (HTML) is known for its organized structure. Though not considered a programming language, it is used to create websites, especially when paired with CSS and JavaScript.")
        result_text.insert(INSERT, "\n\nLearn HTML here at: https://www.w3schools.com/html/default.asp!")
    
    result_text.pack()

def launch_quiz():
  # set up window
  win = Toplevel()
  win.geometry("800x400")
  win.title("Tell Us Your Preferences And We'll Tell You What Language You Should Be Coding In")
  
  # set up scrollbar
  obj = ScrollableFrame(win, height=3200, width=800)
  win = obj.frame
  
  # set emojis
  CRYING_FACE = '\U0001F62D'
  SLIPPER = '\U0001FA74'
  SWEARING_FACE = '\U0001F92C'
  MOUNTAIN = '\u26f0' + '\ufe0f'
  SILHOUETTE = '\U0001F464'
  MAN = '\U0001F64E'+ '\U0001F3FB' + '\u200d' + '\u2642' + '\ufe0f' # a man pouting in light skin tone
  BREAKFAST_BOWL = '\U0001F963'
  PANCAKES = '\U0001F95E'
  EGGS = '\U0001F373'
  TOAST = '\U0001F25E' # there's no chocolate toast emoji, but bread is close
  
  ##flag emojis are combinations of regional indictator characters
  FLAG_UA = '\U0001F1FA' + '\U0001F1E6'
  FLAG_ES = '\U0001F1EA' + '\U0001F1F8'
  FLAG_DK = '\U0001F1E9' + '\U0001F1F0'
  FLAG_VA = '\U0001F1FB' + '\U0001F1E6'
  
  HEADPHONES = '\U0001F3A7'
  GUITAR = '\U0001F3B8'
  MIC = '\U0001F3A4'
  NOTES = '\U0001F3B6'
  GAME = '\U0001F3AE' # a video game controller
  BIRD = '\U0001F426'
  BABY = '\U0001F476' # the Reddit logo kind of looks like the baby emoji...
  GOGGLES = '\U0001F97D' # ...and the Discord logo reminds me of goggles...
  PIN = '\U0001F4CC'
  MATH = '\U0001F9EE' # the abacus emoji
  GRAPH = '\U0001F4C8'
  BOOK = '\U0001F4D6'
  
  # set up questions
  Question(win, 1, "Pick a Steven He quote", [Option('E-MOTIONAL DA-MAGE!', 'emotional_damage.gif'), Option('I will send you to Jesus...', 'i_will_send_you.gif'), Option('What the hail?!', 'what_the_hail.gif'), Option('Before physics was invented...', 'before_physics.gif')], 1)
  Question(win, 2, "Pick a Greek philosopher", [Option('Pythagoras', 'pythagoras.gif'), Option('Socrates', 'socrates.gif'), Option('Plato', 'plato.gif'), Option('Aristotle', 'aristotle.gif')], 1)
  Question(win, 3, "Pick an actor who played Spiderman", [Option('Toby McGuire', 'toby_mcguire.gif'), Option('Tom Holland', 'tom_holland.gif'), Option('Andrew Garfield', 'andrew_garfield.gif'), Option('Peter Parker', 'peter_parker.gif')], 1)
  Question(win, 4, "Pick a breakfast meal", [Option('Oatmeal', 'oatmeal.gif'), Option('Pancakes', 'pancakes.gif'), Option('Chocolate Toast', 'chocolate_toast.gif'), Option('Eggs', 'eggs.gif')], 1)
  Question(win, 5, "Pick a flag of a country in Europe", [Option("Ukraine", 'ukraine_flag.gif'), Option("Spain", 'spain_flag.gif'), Option("Denmark", 'denmark_flag.gif'), Option("Vatican City", 'vatican_flag.gif')], 1)
  Question(win, 6, "Pick a genre of music", [Option('Lofi', 'lofi.gif'), Option('Rock', 'rock.gif'), Option('Rap', 'rap.gif'), Option('Blues', 'blues.gif')], 1)
  Question(win, 7, "Pick a multiplayer game", [Option('Skribbl.io', 'skribblio.gif'), Option('Among Us', 'amogus.gif'), Option('Animal Crossing', 'animal_crossing.gif'), Option('Slither.io', 'slitherio.gif')], 1)
  Question(win, 8, "Pick a social media site", [Option('Twitter', 'twitter_logo.gif'), Option('Reddit', 'reddit_logo.gif'), Option('Discord', 'discord_logo.gif'), Option('Pinterest', 'pinterest_logo.gif')], 1)
  Question(win, 9, "Pick a calculus concept", [Option('Derivatives', 'derivatives.gif'), Option('Integrals', 'integrals.gif'), Option('Limits', 'limits.gif'), Option('Graphing', 'graphing.gif')], 1)
  Question(win, 10, "Pick a Charles Dickens novel", [Option('A Tale of Two Cities', 'a_tale_of_two_cities.gif'), Option('Oliver Twist', 'oliver_twist.gif'), Option('Great Expectations', 'great_expectations.gif'), Option('Bleak House', 'bleak_house.gif')], 2)
  
  # submit button
  submit_btn = Image.open("images/submit_button.gif").resize((270,100))
  SUBMIT_BTN = ImageTk.PhotoImage(submit_btn)
  
  submit = Button(win, image=SUBMIT_BTN, command=finish_quiz)
  submit.image = SUBMIT_BTN
  submit.place(x=400, y=3100, anchor='c')

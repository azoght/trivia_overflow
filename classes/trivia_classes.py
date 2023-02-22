'''
Classes representing componnents of trivia

Posts contain a trivia question, as well as its responses
Trivia Questions are multiple choice, and there can only be one answer
Responses are made by users who didn't create the post
Trivia Faucets retrieve questions using the Open Trivia Database API
'''
import uuid  # for random ids
import requests # to fetch information from URLs
import ast # to evaluate Trivia API requests
import base64 # to decode base64 encoding
import random

class Post:

  def __init__(self, question, author_name, date_posted, quota):
    self.author_name = author_name
    self.date_posted = date_posted
    self.question = question
    self.quota = quota
    self.responses = []
    self.id_ = str(uuid.uuid4()) # random UUID (Universal Unique Identifier)

class Response:

  def __init__(self, author_name, answer, date_posted):
    self.author_name = author_name
    self.answer = answer
    self.date_posted = date_posted

class Trivia_Question:

  def __init__(self, header, answers, correct_answer, point_value):
    self.header = header
    self.answers = answers
    self.correct_answer = correct_answer
    self.point_value = point_value
    

class Trivia_Faucet: 

  def __init__(self, num_q, difficulty='any'):
    if difficulty == 'any':
      self.source = ast.literal_eval(requests.get(f"https://opentdb.com/api.php?amount={num_q}&type=multiple&encode=base64").text)
    else:
      self.source = ast.literal_eval(requests.get(f"https://opentdb.com/api.php?amount={num_q}&type=multiple&difficulty={difficulty}&encode=base64").text)

    self.questions = []
    for result in self.source['results']:
      header = str(base64.b64decode(result['question']).decode('utf-8'))
      correct_answer = str(base64.b64decode(result['correct_answer']).decode('utf-8'))
      answers = []
      answers.append(correct_answer)
      for incorrect_answer in result['incorrect_answers']:
        answers.append(str(base64.b64decode(incorrect_answer).decode('utf-8')))
      random.shuffle(answers)

      # sets point value based on difficulty
      if str(base64.b64decode(result['difficulty']).decode('utf-8')) == 'easy':
        point_value = 10
      elif str(base64.b64decode(result['difficulty']).decode('utf-8')) == 'medium':
        point_value = 30
      if str(base64.b64decode(result['difficulty']).decode('utf-8')) == 'hard':
        point_value = 50

      self.questions.append(Trivia_Question(header, answers, correct_answer, point_value))
      
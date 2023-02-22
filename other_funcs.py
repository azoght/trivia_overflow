from test_users import *
from classes.trivia_classes import Trivia_Question, Post

def create_post_from_question(header, answers, correct_answer, point_value, author_name, date_posted, quota=5):
  question = Trivia_Question(header=header, answers=answers, correct_answer=correct_answer, point_value=point_value)
  post = Post(author_name=author_name, date_posted=date_posted, question=question, quota=quota)
  return post

# to get a post based on how its displayed in the posts page

def get_post(post_text, test_posts):
  for post in test_posts:
    if len(post.question.header) > 80: # checks for condensed header
      if "..." in post_text:
        if post_text[:post_text.index("...")] in post.question.header: # everything up to the ellipsis
          return post
    else:
      if post_text[:post_text.index(" [")] == post.question.header: # everything up to the point value
        return post

# to reward users if they respond correctly before post hits quota

def find_user_response_in_post(username, post):
  for response in post.responses:
    if response.author_name == username:
      return response
  return None

# to condense headers that are too long in latest post page

def condense(text):
  if len(text) > 100:
    return text[:100] + "..."
  else:
    return text
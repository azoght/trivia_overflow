'''
Contains all test posts and responses
'''

from classes.trivia_classes import Response
from test_users import other_usernames
from other_funcs import create_post_from_question

p1 = create_post_from_question(header="The creator of the Enigma Cypher and Machine was of what nationality?", answers=['Polish', 'German', 'British', 'American'], correct_answer='German', point_value=20, author_name='TriviaMaster1', date_posted='04/09/2022')

p2 = create_post_from_question(header="What is the name of the popular animatronic singing fish prop, singing such hits as 'Don't Worry, Be Happy'?", answers=['Big Mouth Billy Bass', 'Sardeen', 'Big Billy Bass', 'Singing Fish'], correct_answer='Big Mouth Billy Bass', point_value=20, author_name='TriviaMaster1', date_posted='04/09/2022')

p3 = create_post_from_question(header="What is the name of the 'Flash' and 'Arrow' spinoff from DC featuring a team of characters that have appeared on both shows?", answers=['The Justice Society of America', 'Justice Society', 'Heroes of Tomorrow', 'Legends of Tomorrow'], correct_answer='Legends of Tomorrow', point_value=20, author_name='Loca4Trivia', date_posted='04/08/2022')

test_posts = [p1, p2, p3]

# create test responses

p1.responses.append(Response(author_name= other_usernames[0], answer='C', date_posted="04/09/2022"))
p1.responses.append(Response(author_name= other_usernames[1], answer='B', date_posted="04/09/2022"))

p2.responses.append(Response(author_name= other_usernames[2], answer='D', date_posted="04/09/2022"))
p2.responses.append(Response(author_name= other_usernames[3], answer='A', date_posted="04/09/2022"))

p3.responses.append(Response(author_name= other_usernames[4], answer='B', date_posted="04/09/2022"))
p3.responses.append(Response(author_name= other_usernames[5], answer='C', date_posted="04/08/2022"))

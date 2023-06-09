import os
import slack
import schedule
import time
import pprint
from dotenv import load_dotenv
from slack import WebClient
from slack.errors import SlackApiError
from datetime import datetime
import ssl
import certifi
import openai

# load the .env file to get the token
env_path = ".env"
load_dotenv(env_path)
ssl_context = ssl.create_default_context(cafile=certifi.where())

# get the token from the environment variable
client = slack.WebClient(token=os.environ['SLACK_TOKEN'], ssl=ssl_context)

# get the api key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
  

# Structure to store the data
class Data:
    def __init__(self, id, user, day, month):
        self.id = id
        self.user = user
        self.day = day
        self.month = month

# Data base
people = [
    Data("U058CQ58LMB", "Mario", 22, 5),
	Data("U058Q5FKBRR", "Joao", 21, 5),
	Data("USLACKBOT", "Slackbot", 23, 5),
]

# function to check if there is a birthday today
def check_birthdays():
	
	# Get the current date
	today = datetime.now()

	# Get the people with a birthday today
	birthday_people = [person for person in people if person.day == today.day and person.month == today.month]

	# Check the number of people with a birthday today
	num_people = len(birthday_people)

	# open ai text generation
	response = openai.Completion.create(
  		model="text-davinci-003",
  		prompt="Create an happy birthday message that has less than 30 words.\n",
  		temperature=1.5,
  		max_tokens=30,
  		top_p=1,
  		frequency_penalty=1.5,
  		presence_penalty=1)
	
	ai_text = response.choices[0].text.strip()
	channel = '#test'

	# Generate the birthday message
	if num_people > 1:
    	
		# Multiple people have a birthday today
		mention_list = [f"<@{person.id}|{person.user}>" for person in birthday_people]
		names = ' & '.join(mention_list)
		message = f"{ai_text}\n\n{names} :tada: :confetti_ball: \n\n `text generated by AI`"

		# Generate the birthday message
		client.chat_postMessage(
			channel=channel,
			text=message)
		
	elif num_people == 1:
    	
		# Only one person has a birthday today
		person = birthday_people[0]
		mention = f"<@{person.id}|{person.user}>"
		message = f"{ai_text}\n\n{mention} :tada: :confetti_ball: \n\n `text generated by AI`"
			
		# Generate the birthday message
		client.chat_postMessage(
			channel=channel,
			text=message)


# function to get the list of users
# def users_list():
#     list = client.users_list()

#     if list['ok']:
#         users = list['members']

#         for user in users:
#                 id = user['id']
#                 username = user['profile']['display_name']
#                 print(id, username)
#     else:
#         print(f"Error: {list['error']}")  

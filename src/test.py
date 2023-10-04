import os
from dotenv import load_dotenv
import requests

load_dotenv()
POST_URL = 'https://slack.com/api/chat.postMessage'

requests_body = {'token': os.environ['API_TOKEN'], 'channel': '#90_everything', 'text': 'test!!'}

response = requests.post(POST_URL, data=requests_body)

print(response.json())
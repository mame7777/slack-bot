import os
from dotenv import load_dotenv
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests

POST_URL = 'https://slack.com/api/chat.postMessage'

load_dotenv()
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOCKEN = os.environ['SLACK_APP_TOKEN']

app = App(token=SLACK_BOT_TOKEN)

POST_CHANNEL_NAME = "99_everything"
POST_CHANNEL_ID = ""
CHANNEL_DATA = dict()
USER_DATA = dict()

@app.message("")
def post_message(message, say):
    # get posted user name and icon
    user_name = USER_DATA[message["user"]]["name"]
    user_icon = USER_DATA[message["user"]]["img"]
    
    # get message text
    message_text = message["text"]
    
    # replace mention
    pattern = r"<@.*?>"
    re_result_list = re.findall(pattern, message_text)
    if re_result_list != []:
        for re_result in re_result_list:
            mention_user_id = re_result[2:-1]
            try:
                mention_user_name = USER_DATA[mention_user_id]["name"]
            except KeyError:
                mention_user_name = "unknown user"
            message_text = message_text.replace(re_result, " `@" + mention_user_name + "` ")
    message_text = message_text.replace("<!channel>", " `@channel` ")
    
    # get posted channel name
    try:
        channel_name = CHANNEL_DATA[message["channel"]]
    except KeyError:
        channel_name = "unkown channel"
       
    # post message
    say(
        channel = POST_CHANNEL_ID,
        username = user_name,
        icon_url = user_icon,
        text=f"`#{channel_name}`\n{message_text}"
    )

# if mention
@app.event("app_mention")
def mention(body, say):
    text = body["event"]["text"]
    
    # if include "reload" in mention
    if "reload" in text:
        say(
            channel = POST_CHANNEL_ID,
            username = "Slack Bot (reload)",
            text=f"channelとuserの情報を更新するよ！"
        )
        
        # reload channel and user data
        init()
        
        say(
            channel = POST_CHANNEL_ID,
            username = "Slack Bot (reload)",
            text=f"更新が終わったよ！"
        )

@app.event('message')
def handle_message_events(body, logger):
    logger.info(body)


def init():
    print("initializing...")
    
    # get channel data
    url = "https://slack.com/api/conversations.list?limit=999"
    headres = {"Authorization": "Bearer " + SLACK_BOT_TOKEN}
    response = requests.get(url, headers=headres)
    response_json = response.json()
    global CHANNEL_DATA
    for i in response_json["channels"]:
        CHANNEL_DATA[i["id"]] = i["name"]
        
    # get user data
    url = "https://slack.com/api/users.list"
    headres = {"Authorization": "Bearer " + SLACK_BOT_TOKEN}
    response = requests.get(url, headers=headres)
    response_json = response.json()
    global USER_DATA
    for i in response_json["members"]:
        try:
            USER_DATA[i["id"]] = {"name": i["real_name"], "img": i["profile"]["image_72"]}
        except KeyError:
            USER_DATA[i["id"]] = {"name": i["name"], "img": i["profile"]["image_72"]}
            print("Error: KeyError of getting user name")
    
    print("initialized!")


def main():
    print("start!")
    init()
    global POST_CHANNEL_ID
    POST_CHANNEL_ID = [key for key, value in CHANNEL_DATA.items() if value == POST_CHANNEL_NAME][0]
    
    SocketModeHandler(app, SLACK_APP_TOCKEN).start()
    
if __name__ == "__main__":
    main()
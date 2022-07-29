import random

from dotenv import dotenv_values
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter


config = dotenv_values(".env")

app = Flask(__name__)


slack_events_adapter = SlackEventAdapter(
    config["SLACK_EVENTS_TOKEN"], "/slack/events", app
)

slack_web_client = WebClient(config["SLACKBOT_TOKEN"])
client_id = config["CLIENT_ID"]
client_secret = config["CLIENT_SECRET"]
oauth_scope = config["SLACK_SCOPES"]


MESSAGE_BLOCK = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "*Hello, I'm a bot!*\nI'm here to help you with your tasks.\n\n"
        "I can help you with the following commands:\n"
        "`/todo` - Add a new task\n"
        "`/todo list` - List all tasks\n"
        "`/todo done` - Mark a task as done\n"
        "`/todo undone` - Mark a task as undone\n"
        "`/todo delete` - Delete a task\n"
        "`/todo help` - Show this help message",
    },
}


@app.route("/slack/install", methods=["GET"])
def pre_install():
    state = "randomly_generated_state"
    return f'<a href="https://slack.com/oauth/v2/authorize?scope={oauth_scope}&client_id={client_id}&state={state}">Install</a>'


@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    text = event.get("text")

    if "flip a coin" in text.lower():
        channel_id = event.get("channel")
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Heads"
        else:
            results = "Tails"
        message = f"*Flip a coin:* {results}"

        MESSAGE_BLOCK = ["text"]["text"] = message
        message_to_send = {"channel": channel_id, "blocks": MESSAGE_BLOCK}

    return slack_web_client.chat_postMessage(**message_to_send)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

from flask import Flask, request
import random
from pymessenger.bot import Bot
import os

app = Flask(__name__)
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]
bot = Bot(ACCESS_TOKEN)

# We will recieve messages that Facebook sends out bot at this endpoint
@app.route('/', methods=['GET', 'POST'])
def recieve_message():
    if request.method == 'GET':
        #Before allowing people to message your bot, Facebook has implemented a
        # a verify token that confirms all requests that your bot recieves came
        # from Facebook
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not GET, it must be a POST and we can just proceed with
    # sending a message back to the user
    else:
        #get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:

                if message.get('message'):
                # Facebook Messenger ID for user so we know where to send
                # response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                # if user sends a GIF, photo, video or any other non text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token"

def get_message():
    sample_responses = ["This is it man!", "Way to go!"]
    #return selected item to the user
    return random.choice(sample_responses)

def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


    return "Hello World!"

if __name__ == '__main__':
    app.run()

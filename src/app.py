from helper.openai_api import text_complition
from helper.twilio_api import send_message


from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'


@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    try:
        # Extract incomng parameters from Twilio
        message = request.form['Body']
        print(message)
        sender_id = request.form['From']
        print(sender_id)

        # Get response from Openai
        result = text_complition(message)
        # print(result,result['status'])
        if result['status'] == 1:
            send_message(sender_id, result['response'])
    except:
        pass
    return 'OK', 200

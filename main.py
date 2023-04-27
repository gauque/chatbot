# import flask dependencies
import flask
from flask import Flask
from flask import request, jsonify
import os
import google.cloud.dialogflow_v2beta1 as dialogflow
import requests
from twilio.rest import Client

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'key.json'

DIALOGFLOW_PROJECT_ID ='asistentecomercial-fnia'
DIALOGFLOW_LANGUAGE_CODE = 'es'
SESSION_ID = 'me'

# initialize the flask appp
app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def root():
    return "Hello mi gente linda"

@app.route('/api/recieveMessage')
def recieve_message():
   message=request.form['Body']
   mobnum=request.form["From"]
   return ""

# create a route for webhook
@app.route('/api/getMessage', methods=['GET', 'POST'])
def home():
   message=request.form.get('Body') #Get message from the user
   mobnum=request.form.get('From') #Who is the user (phone)
   #Create and configure Dialogflow Session
   session_client = dialogflow.SessionsClient() 
   session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
   text_input = dialogflow.types.TextInput(text=message, language_code=DIALOGFLOW_LANGUAGE_CODE)
   query_input = dialogflow.types.QueryInput(text=text_input)
   try:
      response = session_client.detect_intent(session=session, query_input=query_input)
   except dialogflow.exceptions.InvalidArgument as e:
      raise
 
   print ("Query text:", response.query_result.query_text)
   print("Detected intent:", response.query_result.intent.display_name)
   print("Detected intent confidence", response.query_result.intent_detection_confidence)
   print("Fullfilment text:", response.query_result.fulfillment_text)
   #sendMessage(mobnum, response.query_result.fulfillment_text)

   return response.query_result.fulfillment_text


def sendMessage(mobnum,message):
   account_sid='AC056ac8960010bea0a800750bb945c8b7'
   auth_token='cac8a04564614b7d4b8e8e4806c5bfcd'
   client=Client(account_sid, auth_token)
   if not mobnum.startswith('whatsapp:'):
      mobnum='whatsapp:' + mobnum

   message= client.messages.create(
      from_='whatsapp:+14155238886',
      body=message,
      to='whatsapp:+573175127124'
   )   


   print(message.sid)
   return "", 200


# run the app
if __name__ == '__main__':
    app.run()
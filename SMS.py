import config
from twilio.rest import Client

client = Client(config.TWILIO_ACCOUNT_SID, config.AUTH_TOKEN)

def send_message(text):
    message = client.messages.create(
             body= text,
             from_= config.TWILIO_PHONE_NUMBER,
             to = config.YOUR_PHONE_NUMBER
         )


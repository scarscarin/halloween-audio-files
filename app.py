from flask import Flask
from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve sensitive data from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(account_sid, auth_token)

phone_number = "+34602210973" 

audio_file_url = "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/spirit_announcement.wav" 

# Flask app to handle the trigger
app = Flask(__name__)

@app.route('/trigger_call', methods=['GET'])
def trigger_call():
    # Make the call
    call = client.calls.create(
        to=phone_number,
        from_=twilio_phone_number,
        url=f"https://handler.twilio.com/twiml/EHbc8d282a68f14d8a4938d4444d9c8ee0?AudioFileUrl={audio_file_url}"
    )
    return f"Call initiated to {phone_number} with audio file {audio_file_url}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

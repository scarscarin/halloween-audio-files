from flask import Flask, request, render_template
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve sensitive data from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

client = Client(account_sid, auth_token)

people = {
    "Marta": "+34602210973",
    "Leo": "+31642153785",
    "Spirit": "+3197008249167",
    "Veerle": "+31648723581",
    "Beer": "+31649903915",
    "Aimée": "+31623387307",
    "Ema": "+393479711348",
    "Soto": "+306940628970",
    "Michael": "+31627967156",
    "Maya": "+31681026547",
    "Pierrot": "+491747095953",
    "Robert": "+31630536378",
    "Sidney": "+393518557207",
    "Claudia": "+40738679900",
    "Ilias": "+381695857711",
    "Irene": "+393299235080",
    "Isabel": "+4798028521",
    "Mina": "+33777762486",
    "Zuza": "+48537193301"
}

audio_files = {
    "Spirit Announcement": "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/spirit_announcement.wav",
    "Aimee call": "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/aimee_call.wav",
    "Jenga": "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/jenga.wav",
    "Claiming Murder": "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/claiming_murder.wav",
    "Donnie Darko": "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/donnie_darko.wav",
    "Leo Died": "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/leo_died.wav",
    "Robert Smells": "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/robert_smells.wav",
    "Contract Found": "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/contract_found.wav",
    "Marta Died":"https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/marta_died.wav",
    "Email Found": "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/email_found.wav",
    "22": "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/22.wav",
    "Isabeeel": "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/isabel.wav"  
}

# Flask app to handle the trigger
app = Flask(__name__)


# Route to display the interface
@app.route('/')
def index():
    return render_template('index.html', people=people, audio_files=audio_files)

# Route to handle the call
@app.route('/make_call', methods=['POST'])
def make_call():
    person = request.form['person']
    audio = request.form['audio']

    # Get the phone number and audio URL
    phone_number = people[person]
    audio_file_url = audio_files[audio]

    # Make the call
    call = client.calls.create(
        to=phone_number,
        from_=twilio_phone_number,
        url=f"https://handler.twilio.com/twiml/EHbc8d282a68f14d8a4938d4444d9c8ee0?AudioFileUrl={audio_file_url}"
    )
    return f"Call initiated to {person} ({phone_number}) with audio '{audio}'"

# Route to handle incoming calls
@app.route('/incoming_call', methods=['POST'])
def incoming_call():
    # Create a Twilio VoiceResponse object
    response = VoiceResponse()

    # Specify the URL of the audio file you want to play
    audio_file_url = "https://github.com/scarscarin/halloween-audio-files/raw/refs/heads/main/audios/22.wav"  # Replace with your actual URL

    # Use the <Play> verb to play the audio file
    response.play(audio_file_url)

    # Return the TwiML response
    return Response(str(response), mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

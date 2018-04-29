import dialogflow
import numpy as np
import os
import random

from collections import OrderedDict
from flask import Flask
from flask import render_template
from flask import session
from flask import send_from_directory
from flask_cors import CORS
from flask_socketio import disconnect
from flask_socketio import emit
from flask_socketio import SocketIO
from google.cloud import speech
from google.cloud import texttospeech
from google.cloud.speech import enums
from google.cloud.speech import types
from scipy.io import wavfile


app = Flask(__name__, static_url_path='')
CORS(app)
app.config['SECRET_KEY'] = 'rezzi secrets'
socketio = SocketIO(app, async_mode='eventlet')


PROJECT_ID = 'rezzi-72934'
SESSION_ID = 44
SAMPLE_RATE = 44100
LANGUAGE = 'en'
AUDIO_OUTPUT_PATH = os.path.join(os.path.abspath('./static/audio'), 'out.wav')
AUDIO_RESPONSE_BASE = os.path.abspath('./static/audio')

SESSION_CLIENT = dialogflow.SessionsClient()
SESSION = SESSION_CLIENT.session_path(PROJECT_ID, SESSION_ID)

DATA = {}


@app.route('/')
def index():
    return render_template('rezzi.html')


@app.route('/static/audio<path:path>')
def send_mp3(path):
    return send_from_directory('static', path)


@socketio.on('connect')
def connect():
    session['audio'] = []


@socketio.on('sample_rate')
def handle_my_sample_rate(sampleRate):
    session['sample_rate'] = sampleRate


@socketio.on('audio')
def handle_my_custom_event(audio):
    values = OrderedDict(
        sorted(audio.items(), key=lambda t: int(t[0]))).values()
    session['audio'] += values


@socketio.on('disconnect_request')
def test_disconnect():
    sample_rate = session['sample_rate']
    my_audio = np.array(session['audio'], np.float32)
    sindata = np.sin(my_audio)
    scaled = np.round(32767 * sindata)
    newdata = scaled.astype(np.int16)
    wavfile.write(AUDIO_OUTPUT_PATH, sample_rate, newdata)

    query, params, fulfillment = detect_intent_audio(sample_rate=sample_rate)
    for p_k, p_v in params.items():
        if p_k in ["language", "jobs", "date-period"]:
            DATA[p_k] = str(p_v)
        else:
            DATA[p_k] = [p_v]

    print("NEW DATA", DATA)

    filename = synthesize_text(fulfillment)
    emit('my_response', {'data': f"/audio/{filename}", 'query': query,
                         'answer': fulfillment})
    session['audio'] = []
    disconnect()


def speech_to_text(sample_rate=SAMPLE_RATE, file_name=AUDIO_OUTPUT_PATH):
    client = speech.SpeechClient()

    with open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code='en-US')

    response = client.recognize(config, audio)

    text = []
    for result in response.results:
        text.append(result.alternatives[0].transcript)
        print('Transcript: {}'.format(result.alternatives[0].transcript))

    return text


def detect_intent_audio(project_id=PROJECT_ID, session_id=SESSION_ID,
                        audio_file_path=AUDIO_OUTPUT_PATH,
                        language_code=LANGUAGE, sample_rate=SAMPLE_RATE):
    """Returns the result of detect intent with an audio file as input.

    Using the same `session_id` between requests allows continuation
    of the conversaion.
    """

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = sample_rate

    with open(audio_file_path, 'rb') as audio_file:
        input_audio = audio_file.read()

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)
    query_input = dialogflow.types.QueryInput(audio_config=audio_config)

    response = SESSION_CLIENT.detect_intent(
        session=SESSION, query_input=query_input,
        input_audio=input_audio)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))

    return (response.query_result.query_text, response.query_result.parameters,
            response.query_result.fulfillment_text)


def detect_intent_texts(project_id=PROJECT_ID, session_id=SESSION_ID,
                        texts=['hello'], language_code=LANGUAGE):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversaion.
    """
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))


def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    filename = f'resp_{random.randint(0, 999999)}.mp3'
    filepath = os.path.join(AUDIO_RESPONSE_BASE, filename)

    with open(filepath, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {filepath}')

    return filename


if __name__ == '__main__':
    socketio.run(app, debug=True)

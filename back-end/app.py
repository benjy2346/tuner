from flask import Flask
from flask_socketio import SocketIO
import numpy as np 
# import aubio

app = Flask(__name__)
socketio = SocketIO(app)

# Aubio pitch detection
def detect_pitch(audio_data):
    return 1000
    pitch_detector = aubio.pitch("default", 2048, 2048, 44100)
    pitch_detector.set_unit("Hz")
    
    # Convert raw audio data into numpy array for pitch detection
    audio_array = np.frombuffer(audio_data, dtype=np.float32)
    pitch = pitch_detector(audio_array)[0]
    
    return pitch

# WebSocket route to handle the incoming audio stream
@socketio.on('message')
def handle_audio_stream(audio_data):
    pitch = detect_pitch(audio_data)  # Detect pitch from the audio data
    print(f"Detected pitch: {pitch} Hz")

    # Send feedback back to the front-end
    socketio.send({'pitch': pitch})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

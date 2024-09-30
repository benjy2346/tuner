from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Handle WebSocket connection for namespace /audio-stream
@socketio.on('connect', namespace='/audio-stream')
def handle_connect():
    print('Client connected to /audio-stream')

@socketio.on('disconnect', namespace='/audio-stream')
def handle_disconnect():
    print('Client disconnected from /audio-stream')

# Handle audio data stream
@socketio.on('message', namespace='/audio-stream')
def handle_audio_stream(audio_data):
    # Here you would process the audio data
    print('Received audio data')
    socketio.send('Pitch detected', namespace='/audio-stream')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)

from flask import Flask, render_template, request
from flask_socketio import SocketIO
import random
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# Global flag to control typing
typing_active = False

def simulate_typing(text, speed):
    global typing_active
    typing_active = True
    
    # Define typing speeds - made fast mode much faster
    speeds = {
        "slow": (0.1, 0.3),
        "normal": (0.05, 0.15),
        "fast": (0.005, 0.01)  # Significantly reduced delays for fast mode
    }
    min_delay, max_delay = speeds[speed]
    
    # Type each character
    for char in text:
        if not typing_active:
            break
        time.sleep(random.uniform(min_delay, max_delay))
    
    if typing_active:
        socketio.emit('typing_complete')
    
    typing_active = False

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('start_typing')
def handle_typing_request(data):
    global typing_active
    # Stop any ongoing typing
    typing_active = False
    time.sleep(0.5)  # Wait for previous typing to stop
    
    # Start new typing thread
    text = data['text']
    speed = data['speed']
    threading.Thread(target=simulate_typing, args=(text, speed)).start()
    return {'status': 'started'}

@socketio.on('stop_typing')
def handle_stop_request():
    global typing_active
    typing_active = False
    return {'status': 'stopped'}

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')

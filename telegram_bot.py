import requests
import time
import os
import threading
from flask import Flask

app = Flask(__name__)

# Bot token and chat ID
TOKEN = os.getenv('TOKEN', '8361902202:AAH8KJW9_6ixm140bRmwY1Jz52kwHns-GqM')
CHAT_ID = os.getenv('CHAT_ID', '@noselovea')  # Public group username

# List of files to send
files = [
    'dishapatani_501003465_18520526083013912_2698487590039069318_n-2025-05-6e3beacfff0adfdf9b1b55ab38b2403b.jpg',
    'photo_2025-03-19_13-22-00.jpg',
    'video_2025-01-16_14-32-37.mp4',
    'IMG_20230901_231855_591-01.jpeg'
]

def send_file(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'  # Use sendDocument for files
    with open(file_path, 'rb') as f:
        files_data = {'document': f}
        data = {'chat_id': CHAT_ID}
        response = requests.post(url, data=data, files=files_data)
        print(response.json())

def bot_loop():
    index = 0
    while True:
        if index >= len(files):
            index = 0  # Loop back to start
        send_file(files[index])
        index += 1
        time.sleep(600)  # 10 minutes

@app.route('/')
def home():
    return "Bot is running!"

if __name__ == '__main__':
    # Start bot in a thread
    threading.Thread(target=bot_loop, daemon=True).start()
    # Run Flask app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
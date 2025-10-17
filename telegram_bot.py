import requests
import time
import os
import threading
from flask import Flask, request, jsonify, render_template
from mega import Mega

app = Flask(__name__)

# Bot token and chat ID
TOKEN = os.getenv('TOKEN', '8361902202:AAH8KJW9_6ixm140bRmwY1Jz52kwHns-GqM')
CHAT_ID = os.getenv('CHAT_ID', '@noselovea')  # Public group username

# Mega credentials
MEGA_EMAIL = os.getenv('MEGA_EMAIL')
MEGA_PASSWORD = os.getenv('MEGA_PASSWORD')
mega = Mega()
m = mega.login(MEGA_EMAIL, MEGA_PASSWORD) if MEGA_EMAIL and MEGA_PASSWORD else None

# List of files to send
files = [
    'dishapatani_501003465_18520526083013912_2698487590039069318_n-2025-05-6e3beacfff0adfdf9b1b55ab38b2403b.jpg',
    'photo_2025-03-19_13-22-00.jpg',
    'video_2025-01-16_14-32-37.mp4',
    'IMG_20230901_231855_591-01.jpeg'
]

def send_file(file_path):
    if file_path.startswith('http'):  # If it's a URL from Mega
        url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
        data = {'chat_id': CHAT_ID, 'text': file_path}
        response = requests.post(url, data=data)
        print(response.json())
        return

    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    ext = os.path.splitext(file_path)[1].lower()
    with open(file_path, 'rb') as f:
        data = {'chat_id': CHAT_ID}
        files_data = {}

        if ext in ['.jpg', '.jpeg', '.png']:
            url = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
            files_data = {'photo': f}
        elif ext in ['.mp4', '.avi', '.mov']:
            url = f'https://api.telegram.org/bot{TOKEN}/sendVideo'
            files_data = {'video': f}
        elif ext == '.gif':
            url = f'https://api.telegram.org/bot{TOKEN}/sendAnimation'
            files_data = {'animation': f}
        elif ext == '.webp':
            url = f'https://api.telegram.org/bot{TOKEN}/sendSticker'
            files_data = {'sticker': f}
        else:
            url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
            files_data = {'document': f}

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
    return render_template('index.html')

@app.route('/files')
def get_files():
    return jsonify(files)

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist('files')
    for file in uploaded_files:
        if file:
            filename = file.filename
            file_path = os.path.join('.', filename)
            file.save(file_path)
            if m:
                # Upload to Mega
                folder = m.find('telegram_files') or m.create_folder('telegram_files')
                m.upload(file_path, folder[0])
                link = m.get_link(m.find(filename, folder[0]))
                files.append(link)
                os.remove(file_path)  # Delete local file
            else:
                files.append(filename)
    return '', 204

if __name__ == '__main__':
    # Start bot in a thread
    threading.Thread(target=bot_loop, daemon=True).start()
    # Run Flask app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
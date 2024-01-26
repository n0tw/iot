from flask import Flask, request
import requests
import schedule
import time

app = Flask(__name__)

# Replace 'YOUR TELEGRAM BOT TOKEN' with your actual Telegram Bot token
TOKEN = '6971283115:AAGHpKPd5hXSbDf6afYORNbIK7oohLrjwiI'
TELEGRAM_API_BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

def read_words_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            words = file.read().splitlines()
        return words
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

def save_words_to_file(file_path, words):
    with open(file_path, 'w') as file:
        for word in words:
            file.write(word + '\n')

def collect_chat_ids():
    file_path = 'chatIds.txt'  # Change this to the path of your txt file

    # Read words from the file
    chat_ids = read_words_from_file(file_path)
    print("Current chat IDs in the list:")
    print(chat_ids)

    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    data = requests.get(url).json()
    for doc in data:
        if doc['message']['chat']['id'] not in chat_ids:
            chat_ids.append(doc['message']['chat']['id'])

    # Save the updated list back to the file
    save_words_to_file(file_path, chat_ids)
    print("Updated chat IDs have been saved to the file.")

def job():
    collect_chat_ids()

# Schedule the job to run every 20 seconds
schedule.every(20).seconds.do(job)

@app.route('/forward_notification', methods=['POST'])
def forward_notification():
    global chat_ids
    data = request.get_json()
    print(data)
    for chatID in chat_ids:
        print(requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chatID}&text={data['data']['message']}").json())
    return '', 200

if __name__ == '__main__':
    # Run the Flask app in a separate thread
    import threading
    threading.Thread(target=app.run, kwargs={'port': 3000}).start()

    # Run the scheduled job in the main thread
    while True:
        schedule.run_pending()
        time.sleep(1)
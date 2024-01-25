from flask import Flask, request
import requests

app = Flask(__name__)

# Replace 'YOUR TELEGRAM BOT TOKEN' with your actual Telegram Bot token
TOKEN = '6971283115:AAGHpKPd5hXSbDf6afYORNbIK7oohLrjwiI'
TELEGRAM_API_BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"
# The following link was assigned from ngrok after installing it and running (ngrok http 3000) in terminal.
# This way, the port 3000 becomes exposed to the public.
NGROK_PUBLIC_URL = "https://543f-2a02-587-796f-2100-dcfc-c0f2-e12-a332.ngrok-free.app/"

chat_ids = []

@app.route('/webhook', methods=['POST'])
def webhook():
    global chat_ids
    data = request.get_json()
    # Process the received update as needed
    print("Received update:", data)
    if data['message']['chat']['id'] not in chat_ids:
        chat_ids.append(data['message']['chat']['id'])
    return '', 200

@app.rout('/forward_notification', methods=['POST'])
def forward_notification():
    global chat_ids
    data = request.get_json()
    if data['data'] == "":
        for chatID in chat_ids:
            print(requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chatID}&text={data['message']}").json())
    return '', 200

if __name__ == '__main__':
    set_webhook_url = f"{TELEGRAM_API_BASE_URL}setWebhook?url={NGROK_PUBLIC_URL}/webhook"

    print(requests.get(set_webhook_url).json())

    app.run(port=3000)
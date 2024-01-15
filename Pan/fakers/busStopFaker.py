import requests
from flask import Flask, jsonify, request
import schedule
import time

app = Flask(__name__)

# Define the endpoint to receive data
@app.route('/receive_data', methods=['POST'])
def receive_data():
    try:
        # Get the data from the POST request
        data = request.get_json()

        # Post the received data to the edge controller
        post_to_edge_controller(data)

        # Respond to the original request
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Function to post data to the edge controller
def post_to_edge_controller(data):
    edge_controller_url = 'http://localhost:5000/receive_data'  # Adjust the URL as needed
    response = requests.post(edge_controller_url, json=data)
    response.raise_for_status()

# Function to post data to a different endpoint every 5 seconds
def post_periodically():
    edge_controller_url = 'http://localhost:5000/another_endpoint'  # Adjust the URL as needed
    data_to_send = {'key': 'value'}  # Adjust the data as needed
    response = requests.post(edge_controller_url, json=data_to_send)
    response.raise_for_status()

# Schedule the periodic job
schedule.every(5).seconds.do(post_periodically)

# Function to run the scheduled jobs
def run_scheduled_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Run the Flask app on port 5001 in a separate thread
    from threading import Thread
    Thread(target=app.run, kwargs={'port': 5001}).start()

    # Run the scheduled jobs in the main thread
    run_scheduled_jobs()

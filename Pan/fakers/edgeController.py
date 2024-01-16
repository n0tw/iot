from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Define the endpoint where you receive HTTP POST messages
@app.route('/receive_bus_data', methods=['POST'])
def receive_bus_data():
    try:
        # Get the data from the POST request
        data = request.get_json()
        print(data)
        # Edit the data (modify as per your requirements)
        #edited_data = edit_data(data)

        # Post the edited data to another endpoint
        #post_to_endpoint(edited_data, 'https://example.com/other_endpoint')

        # Respond to the original request
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/receive_station_data', methods=['POST'])
def receive_station_data():
    try:
        # Get the data from the POST request
        data = request.get_json()
        print(data)
        # Edit the data (modify as per your requirements)
        #edited_data = edit_data(data)

        # Post the edited data to another endpoint
        #post_to_endpoint(edited_data, 'https://example.com/other_endpoint')

        # Respond to the original request
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/receive_crowd_data', methods=['POST'])
def receive_crowd_data():
    try:
        # Get the data from the POST request
        data = request.get_json()
        print(data)
        # Edit the data (modify as per your requirements)
        #edited_data = edit_data(data)

        # Post the edited data to another endpoint
        #post_to_endpoint(edited_data, 'https://example.com/other_endpoint')

        # Respond to the original request
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/receive_violation_data', methods=['POST'])
def receive_violation_data():
    try:
        # Get the data from the POST request
        data = request.get_json()
        print(data)
        # Edit the data (modify as per your requirements)
        #edited_data = edit_data(data)

        # Post the edited data to another endpoint
        #post_to_endpoint(edited_data, 'https://example.com/other_endpoint')

        # Respond to the original request
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

# Function to post data to another endpoint
def post_to_endpoint(data, endpoint):
    response = requests.post(endpoint, json=data)
    response.raise_for_status()

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(port=5000)

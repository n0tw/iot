const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const fetch = require('node-fetch');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);


app.use(bodyParser.json());
app.use(cors({
    origin: 'http://127.0.0.1:8000',
    credentials: true,
    allowedHeaders: ['Content-Type', 'Authorization'],
}));

app.post('/subscribe', async (req, res) => {
    const subscriptionData = req.body; // Data for context broker subscription
    const contextBrokerUrl = 'http://150.140.186.118:1026/v2/subscriptions';

    try {
        const response = await fetch(contextBrokerUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(subscriptionData),
        });

        const responseData = await response.text();

        // Check if the response body is empty or not JSON
        if (!responseData || !response.headers.get('content-type')?.includes('application/json')) {
            console.log('Unexpected or empty response:', responseData);
            res.status(500).json({ error: 'Unexpected or empty response from Orion Context Broker' });
            return;
        }

        // Parse the JSON response
        const jsonResponse = JSON.parse(responseData);
        res.json(jsonResponse);
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

const stations = [
    {
        id: "urn:ngsi-ld:Station:Station:MNCA-STram-L02-AP-T2",
        name: "Zaimi"
    },
    {
        id: "urn:ngsi-ld:Station:Station:MNCA-STram-L02-AP-T3",
        name: "Pritaneia"
    },
    {
        id: "urn:ngsi-ld:Station:Station:MNCA-STram-L02-AP-T4",
        name: "Ermou"
    }
];

const buses = [
    {
        id: "urn:ngsi-ld:Vehicle:vehicle:WasteManagement:1",
        name: "Bus1"
    },
    {
        id: "urn:ngsi-ld:Vehicle:vehicle:WasteManagement:2",
        name: "Bus2"
    },
    {
        id: "urn:ngsi-ld:Vehicle:vehicle:WasteManagement:3",
        name: "Bus3"
    }
];

io.on('connection', (socket) => {
    console.log('Client connected');

    // Simulate updates with station names
    setInterval(() => {
        const randomStationIndex = Math.floor(Math.random() * stations.length);
        const station = stations[randomStationIndex];

        // Simulate data received from the context broker
        const data = {
            stationName: station.name,
            attributeValue: Math.floor(Math.random() * 100), // Example random attribute value
            entityAttribute: "crowdFlowObserved", // Example entity attribute
            changeInValue: "+5", // Example change in value
        };

        // Emit the 'update' event with station name
        socket.emit('update', data);
    }, 5000); // Simulate updates every 5 seconds

    setInterval(() => {
        const randomStationIndex = Math.floor(Math.random() * stations.length);
        const bus = buses[randomStationIndex];

        // Simulate data received from the context broker
        const busdata = {
            busName: bus.name,
            attributeValues: {lgn: Math.floor(Math.random() * 100),lat: Math.floor(Math.random() * 100)}, // Example random attribute value
            entityAttribute: "location"
        };
        socket.emit('buslocation', busdata);
    }, 3000);

    // Handle disconnection
    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

// Your existing subscriptionData
const subscriptionData = {
    "subject": {
        "entities": [
            {
                "id": "urn:ngsi-ld:Station:Station:MNCA-STram-L02-AP-T2",
                "type": "TransportStation",
                "condition": {
                    "attrs": [
                        "location"
                    ]
                }
            }
        ]
    },
    "notification": {
        "http": {
            "url": "http://127.0.0.1:8000"
        }
    }
};


// Fetch subscription
fetch('http://150.140.186.118:1026/v2/subscriptions', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(subscriptionData),
})
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

// Start the server
const PORT = 8000;
server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

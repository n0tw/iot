const express = require('express');
const cors = require('cors');
const axios = require('axios');
const bodyParser = require('body-parser');
const fetch = require('node-fetch');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);
const nodemailer = require('nodemailer');

const PORT = 8080;

app.use(bodyParser.json());
app.use(cors({
    origin: 'http://127.0.0.1:8080',
    credentials: true,
    allowedHeaders: ['Content-Type', 'Authorization'],
}));

const transporter = nodemailer.createTransport({
    pool: true,
    service: 'hotmail',
    auth: {
      user: 'evgenia.123@hotmail.com',
      pass: '6ab]~+@^@2Ta5l96VV32wgw9FvO/R|_8',
    },
    tls: {
        rejectUnauthorized: false
    }
});

const readEntityAttribute = async (entityId, attributeName) => {
    try {
      const response = await axios.get(`http://150.140.186.118:1026/v2/entities/${entityId}`);
      
      console.log('Full response:', response.data);
  
      // Check if the attribute exists in the response
      if (response.data && response.data[attributeName]) {
        const attributeValue = response.data[attributeName].value;
        /* console.log(`Attribute ${attributeName} value:`, attributeValue); */
        return attributeValue;
      } else {
        console.log(`Attribute ${attributeName} not found for entity ${entityId}`);
        return null;
      }
    } catch (error) {
      console.error('Error reading entity attribute:', error.message);
      return null;
    }
};
const monitorAttribute = async (stationids) => {
    let text='';
    try {
        // Use Promise.all to wait for all attribute fetching operations
        await Promise.all(stationids.map(async (id) => {
            try {
                const observationDateTime = await readEntityAttribute(await readEntityAttribute(id, 'trafficViolation'), 'observationDateTime');
                const vehiclePlate = await readEntityAttribute(await readEntityAttribute(id, 'trafficViolation'), 'vehiclePlate');
                const transportStation = await readEntityAttribute(id, 'name');

                text = text + `Illegal parking detected in ${transportStation} at ${observationDateTime['@value']}. The vehicle of interest has the following plate number: ${vehiclePlate}.\n\n`;
            } catch (attributeError) {
                console.error(`Error fetching attributes for station ${id}:`, attributeError);
                // Handle or log the error as needed
            }
        }));

        const mailOptions = {
            from: 'evgenia.123@hotmail.com',
            to: 'evgenia.123@hotmail.com',
            subject: 'Illegal parking in bus station',
            text: text,
        };

        setTimeout(() => {
            transporter.sendMail(mailOptions, (error, info) => {
                if (error) {
                    console.error('Error sending email:', error);
                } else {
                    console.log('Email sent:', info.response);
                    violations.push(filteredStations);
                }
            });
        }, 10000);
    } catch (error) {
        console.error('Error monitoring attribute:', error);
    }
};

app.post('/notification-endpoint', async (req, res) => {
    console.log('Received notification:', req.body);
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
let stationData = [];
let violations = [];

const updateStationData = async () => {
    try {
        stationData = await Promise.all(stations.map(async (station) => {
            const illparkingid = await readEntityAttribute(station.id, 'trafficViolation') || '-';

            return {
                id: station.id,
                peopleCount: await readEntityAttribute(await readEntityAttribute(station.id, 'crowdFlowObserved'), 'peopleCount'),
                congested: await readEntityAttribute(await readEntityAttribute(station.id, 'crowdFlowObserved'), 'congested'),
                illparking: await readEntityAttribute(await readEntityAttribute(station.id, 'trafficViolation'), 'description'),
                illparkingid: illparkingid,
                name: await readEntityAttribute(station.id, 'name')
            };
        }));

        const filteredStations = stationData.filter(station => station.illparkingid !== '-' && !violations.includes(station.id));
        const removeStations = stationData.filter(station => station.illparkingid === '-' && violations.includes(station.id));
        violations = violations.filter(e => !removeStations.map(station => station.id).includes(e));

        
        filteredStations.forEach(station => {
            violations.push(station.id);
        });
        monitorAttribute(violations);

    } catch (error) {
        console.error('Error updating station data:', error.message);
    }
};


updateStationData();

/* app.get('/getStationInfo', async (req, res) => {
    res.json(stationData);
}); */

io.on('connection', (socket) => {
    console.log('Client connected');
    /* socket.on('update', (data) => {
        console.log('Received update:', data);
    }); */

    setInterval(() => {
        updateStationData(); 
        socket.emit('update', stationData);
    }, 6000);

    setInterval(() => {
        const randomStationIndex = Math.floor(Math.random() * buses.length);
        const bus = buses[randomStationIndex];

        const busdata = {
            busName: bus.name,
            attributeValues: {lgn: Math.floor(Math.random() * 100),lat: Math.floor(Math.random() * 100)}, 
            entityAttribute: "location"
        };
        socket.emit('buslocation', busdata);
    }, 3000);

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});


server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

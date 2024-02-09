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

const stations = [];
const buses = [];
let stationData = [];
let busData = [];
let buslasts = [];
let violations = [];
let congestions = [];

app.use(bodyParser.json());
app.use(cors({
    origin: 'http://127.0.0.1:8080',
    credentials: true,
    allowedHeaders: ['Content-Type', 'Authorization'],
}));
app.use(cors({
    origin: 'http://127.0.0.1:8000',
    credentials: true,
    allowedHeaders: ['Content-Type', 'Authorization'],
}));

/* const changePeopleCount= async (entityId, updatedValue) => {
    fetch(`http://150.140.186.118:1026/v2/entities/${entityId}/attrs`, {
        method: 'PATCH', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            peopleCount: {
                "type": "Property",
                "value": updatedValue
            }
        }),
    })
    .then(response => {
        if (response.ok) {
            console.log(`Attribute 'peopleCount' of entity ${entityId} updated successfully`);
        } else {
            console.error(`Failed to update attribute 'peopleCount' of entity ${entityId}. Status: ${response.status}`);
        }

        return response.text();
    })
    .then(responseText => console.log('Response Body:', responseText))
    .catch(error => console.error('Error:', error));
};
 */
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



app.get('/getStationInfo', async (req, res) => {
    console.log('GET /getStationInfo called');
    res.json(stationData);
});
app.get('/getBusInfo', async (req, res) => {
    res.json(busData);
}); 

const readBusPCinfo = async (entityId) => {
    try {
        
        const lS = await readEntityAttribute((await readEntityAttribute(entityId, "crowdFlowObserved")).value, 'name');
        const dT = await readEntityAttribute((await readEntityAttribute(entityId, "crowdFlowObserved")).value, 'dateObserved');
        const pC = await readEntityAttribute((await readEntityAttribute(entityId, "crowdFlowObserved")).value, 'peopleCount');
        console.log("name", await readEntityAttribute((await readEntityAttribute(entityId, "crowdFlowObserved")).value, 'name'));
        return {
            lastStation: lS,
            dateTime: dT,
            peopleCount: pC
        };
        
    }catch (error) {
        console.error(`Error in readBusPCinfo ${entityId} :`, error.message);
        return null;
    }
}

app.get('/getBusPC', async (req, res) => {
    try {
        const buslasts = await readBusPCinfo(req.query.id);
        console.log(buslasts);
        res.json(buslasts);
    } catch (error) {
        console.error('Error:', error.message);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

const readEntityAttribute = async (entityId, attributeName) => {
    try {
      const response = await axios.get(`http://150.140.186.118:1026/v2/entities/${entityId}`);
      
      //console.log('Full response:', response.data[attributeName]);
  
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
      console.error(`Error reading entity attribute ${entityId} ${attributeName}:`, error.message);
      return null;
    }
};
const monitorAttribute = async (stationids) => {
    let text='';
    try {
        // Use Promise.all to wait for all attribute fetching operations
        console.log("opopop");
        
        //console.log(readEntityAttribute(await readEntityAttribute(stationids[0], 'trafficViolation')));
        await Promise.all(stationids.map(async (id) => {
            
            try {
                const observationDateTime = await readEntityAttribute((await readEntityAttribute(id, "trafficViolation")).value, 'observationDateTime');
                const vehiclePlate = await readEntityAttribute((await readEntityAttribute(id, "trafficViolation")).value, 'vehiclePlate');
                const transportStation = await readEntityAttribute(id, 'name');

                text = text + `Illegal parking detected in ${transportStation.value} at ${observationDateTime.value['@value']}. The vehicle of interest has the following plate number: ${vehiclePlate}.\n\n`;
            } catch (attributeError) {
                console.log(id);
                console.log(await readEntityAttribute((await readEntityAttribute(id, "trafficViolation")).value, 'observationDateTime'), "+");

                console.error(`Error fetching attributes for station ${id}:`, attributeError);
                
                
                console.log("nnnnnjnjn");
                // Handle or log the error as needed
            }
        }));
        
        const mailOptions = {
            from: 'evgenia.123@hotmail.com',
            to: null,
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






const updateStationData = async () => {
    try {
        stationData = await Promise.all(stations.map(async (station) => {
            //const illparkingid = await readEntityAttribute(station, 'trafficViolation') || '_';
            const illparkingid = await readEntityAttribute(station, 'trafficViolation') || '_';
            //console.log("UpdateSttn", station);
            //console.log("qqqq______________")
            return {
                id: station,
                crowdflowid: await readEntityAttribute(station, 'crowdFlowObserved'),
                illparkingid: illparkingid,
                location: await readEntityAttribute(station, 'location'),
                name: await readEntityAttribute(station, 'name')
            };
            
        }));

        const filteredStations = stationData.filter(station => station.illparkingid.value !== '_' && !violations.includes(station.id));
        const removeStations = stationData.filter(station => station.illparkingid.value === '_' && violations.includes(station.id));
        violations = violations.filter(e => !removeStations.map(station => station.id).includes(e));
        
        console.log("pppppp");
        //console.log(filteredStations[0].illparkingid);
        filteredStations.forEach(station => {
            //console.log("llpar_king",station.illparkingid);
            violations.push(station.id);
        });
        monitorAttribute(violations);

    } catch (error) {
        console.error('updateStationData Error updating station data:', error.message);
    }
};


const updateBusData = async () => {
    try {
        busData = await Promise.all(buses.map(async (bus) => {
            //console.log("mnmnnmnmnmn");
            const congestedid = await readEntityAttribute(bus, 'crowdFlowObserved');
            const locationData = await readEntityAttribute(bus, 'location');
            if (!locationData) {
                return;
            }
            
            return {
                id: bus,
                location: locationData,
                crowdflowid: congestedid,
                license_plate: await readEntityAttribute(bus, 'license_plate')
            };
                
        }));

        const filteredbuss = busData.filter(bus => bus.congested === true && !congestions.includes(bus.id));
        const removebuss = busData.filter(bus => bus.congested === false && congestions.includes(bus.id));
        congestions = congestions.filter(e => {
            CongestionStopped(bus.id);
            !removebuss.map(bus => bus.id).includes(e);
        });

        filteredbuss.forEach(bus => {
            CongestedAllert(bus.id);
            congestions.push(bus.id);
        });

    } catch (error) {
        console.error('Error updating station data:', error.message);
    }
};


const fData = async () => {
    try {
        // Populate the stations array
        for (let i = 1; i < 33; i++) {
            stations.push("urn:ngsild:TransportStation:Station:" + String(i));
            //console.log("uuueueueueue");
            console.log(await readEntityAttribute(stations[i - 1], 'crowdFlowObserved'));
        }

        // Update station data
        await updateStationData();

        // Update the /getStationInfo route with the updated station data
        app.get('/getStationInfo', async (req, res) => {
            console.log('GET /getStationInfo called');
            res.json(stationData);
        });

        

        for (let i = 1; i < 4; i++) {
            buses.push("urn:ngsild:Vehicle:Bus:" + String(i));
            console.log(await readEntityAttribute(buses[i-1], "crowdFlowObserved"));
        }
        await updateBusData();

        app.get('/getBusInfo', async (req, res) => {
            res.json(buses);
        });

    } catch (error) {
        console.error('Error in fData:', error.message);
    }
};
fData();


server.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

async function fetchData() {
    try {
        const response = await fetch('http://localhost:8000/getDataByTime', {
            mode: 'cors',
        });
        const data = await response.json();

        // Log the fetched data
        console.log('Fetched Data:', data);

        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to create and render the chart
async function createChart() {
    const data = await fetchData();

    // Convert xValues to Moment.js objects
    const xValues = data.xValues.map(dateString => moment(dateString));

    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: xValues,
            datasets: [{
                label: 'Data Values',
                data: data.yValues,
                borderColor: 'rgb(75, 192, 192, 0.2)',
                borderWidth: 2,
                fill: false,
            }],
        },
        options: {
            responsive: false,
            scales: {
                x: {
                    type: 'time', // Specify that X-axis values are of type 'time'
                    position: 'bottom',
                },
                y: {
                    beginAtZero: true,
                }
            },
        }
    });
}
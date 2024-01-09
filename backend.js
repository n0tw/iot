const express = require('express');
const cors = require('cors');
const socketIO = require('socket.io');
const axios = require('axios');

const app = express();
const server = require('http').createServer(app);
const io = socketIO(server);

const buses = [
  {
      id: "urn:ngsi-ld:Vehicle:vehicle:WasteManagement:1",
      name: "bus1"
  },
  {
      id: "urn:ngsi-ld:Vehicle:vehicle:WasteManagement:2",
      name: "bus2"
  },
  {
      id: "urn:ngsi-ld:Vehicle:vehicle:WasteManagement:3",
      name: "bus3"
  }
];
let congestions = [];
let busdata = [];
// Asynchronous function to read entity attribute
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

// Asynchronous IIFE to execute async code before starting the server
(async () => {
  // Enable CORS for all routes
  app.use(cors({
    origin: 'http://127.0.0.1:3000', // Update this to match your frontend origin
    credentials: true,
    allowedHeaders: ['Content-Type', 'Authorization'],
  }));

  // Initiate the entity before starting the server
  /* await createEntities('39.556593793150746', '21.767370401805035', '38.24903100595789', '21.7393154225915'); */

  // Read entity attribute
  app.get('/getlocation', async (req, res) => {
    const locationData = await readEntityAttribute('urn:ngsi-ld:Vehicle:vehicle:WasteManagement:1', 'location');
    if (locationData && locationData.coordinates) {
      const coordinates = locationData.coordinates;
      console.log(`Coordinates:`, coordinates);
      res.json({ 
        location: coordinates,
        time: time,
        bus: bus
      });
    } else {
      console.log(`Invalid location data for entity`);
      res.status(500).json({ error: 'Invalid location data' });
    }
  });

  app.get('/getStationInfo', async (req, res) => {
    const stationId = req.query.stationid;
    const locationData = await readEntityAttribute(stationId, 'location');
    const time = await readEntityAttribute(stationId, 'dateLastReported');
    const bus = await readEntityAttribute(stationId, 'vehicleLastReported');
    if (locationData && locationData.coordinates) {
      const coordinates = locationData.coordinates;
      console.log(`Coordinates:`, coordinates);
      res.json({ 
        location: coordinates,
        time: time,
        bus: bus
      });
    } else {
      console.log(`Invalid location data for entity`);
      console.log("stationId", stationId);
      res.status(500).json({ error: 'Invalid location data' });
    }
    console.log(`Attribute location value:`, locationData.coordinates);
    console.log(`Attribute location value:`, time);
    console.log(`Attribute location value:`, bus);
    /* res.json({ 
      location: loctn,
      time: time,
      bus: bus
     }); */

  });
  app.get('/getBusInfo', async (req, res) => {
    res.json(busdata);
  });

  app.get('/googlemaps', async (req, res) => {
    try {
      const { origin, destination, key } = req.query;
      const apiUrl = `https://maps.googleapis.com/maps/api/directions/json?origin=${origin}&destination=${destination}&key=${key}`;
      
      const response = await axios.get(apiUrl);
      res.json(response.data);
    } catch (error) {
      console.error('Error:', error.message);
      res.status(500).json({ error: 'Internal Server Error' });
    }
  });

  const CongestedAllert = async (id) => {
    console.log(`${id} congested!!`);
  };

  const CongestionStopped = async (id) => {
    console.log(`Congestion of ${id} stopped.`);
  };

  const updateBusData = async () => {
    try {
        busdata = await Promise.all(buses.map(async (bus) => {
            const congestedid = await readEntityAttribute(bus.id, 'crowdFlowObserved');
            const locationData = await readEntityAttribute(bus.id, 'location');
            return {
                id: bus.id,
                location: locationData.coordinates,
                peopleCount: await readEntityAttribute(congestedid, 'peopleCount'),
                congested: await readEntityAttribute(congestedid, 'congested'),
                route: await readEntityAttribute(bus.id, 'serviceStatus')
            };
        }));

          const filteredbuss = busdata.filter(bus => bus.congested === true && !congestions.includes(bus.id));
          const removebuss = busdata.filter(bus => bus.congested === false && congestions.includes(bus.id));
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


  updateBusData();
  app.get('/getBusInfo', async (req, res) => {
      res.json(busdata);
  });

  io.on('connection', (socket) => {
    console.log('Client connected');
    setInterval(() => {
        updateBusData();
        socket.emit('busupdate', busdata);
    }, 3000);

    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

  // Start the Express server
  const PORT = 3000;
  server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
  });
})();

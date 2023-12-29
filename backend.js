const express = require('express');
const cors = require('cors');
const axios = require('axios');

const app = express();

const createEntities = async (latitude, longitude) => {
  const entityData = {
    id: 'bus123',
    type: 'Bus',
    location: {
      type: 'geo:point', 
      value: `${latitude},${longitude}`
    }
  };
  try {
    const response = await axios.post('http://150.140.186.118:1026/v2/entities', entityData);
    console.log('Entity created successfully:', response.data);
  } catch (error) {
    console.error('Error creating entity:', error.message);
  }
};

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
  await createEntities('39.556593793150746', '21.767370401805035');

  // Read entity attribute
  app.get('/getlocation', async (req, res) => {
    const loctn = await readEntityAttribute('bus123', 'location');
    console.log(`Attribute location value:`, loctn);
    res.json({ location: loctn });
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
  
  // Start the Express server
  const PORT = 3000;
  app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
  });
})();

const express = require('express');
const mongoose = require('mongoose');
const axios = require('axios');
const cors = require('cors');
const { Chart } = require('chart.js');

const app = express();

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/externalDB', { useNewUrlParser: true, useUnifiedTopology: true });

// Define a MongoDB schema and model (adjust it based on your data structure)
const dataSchema = new mongoose.Schema({
  xValues: [String],
  yValues: [Number],
});

const DataModel = mongoose.model('Data', dataSchema);

// Define a route to get data from MongoDB

const readDataByTime = async(entityId, entityType, initYear, initMonth, initDay, initHour, initMinute, initSecond,
  endYear, endMonth, endDay, endHour, endMinute, endSecond, tz_offset) => {
  try {
    // Make an HTTP request to your Flask API endpoint
    const response = await axios.get(`http://localhost:5000/entities_by_time/${entityId}/${entityType}/${initYear}/${initMonth}
                                      /${initDay}/${initHour}/${initMinute}/${initSecond}/${endYear}/${endMonth}/${endDay}/${endHour}
                                      /${endMinute}/${endSecond}/${tz_offset}`);

    // Retrieve data from the Flask API response
    const dataFromFlask = response.data;

    // Send the data as JSON
    res.json(dataFromFlask);
  } catch (error) {
    console.error('Error fetching data from MongoDB:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

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
  app.get('/getDataByTime', async (req, res) => {
    try {
      const data = await readDataByTime("urn:ngsi-ld:CrowdFlowObserved:Valladolid_1","CrowdFlowObserved",
                                        2018,3,11,15,31,2,2023,4,5,1,5,2,0);

      // Flatten the array of data to get individual entries
      const allEntries = arrayOfDataFromFlask.flatMap(data => data);

      // Extract datetime and peopleCount values
      const xValues = allEntries.map(entry => entry.dateObserved.value['@value']);
      const yValues = allEntries.map(entry => entry.peopleCount.value);

  
      // Create a simple line chart using Chart.js
      const canvasRenderService = new ChartJSNodeCanvas({ width: 800, height: 400 });
      const configuration = {
        type: 'line',
        data: {
          labels: xValues,
          datasets: [{
            label: 'Data Values',
            data: yValues,
            borderColor: 'rgb(75, 192, 192)',
            borderWidth: 2,
            fill: false,
          }],
        },
        options: {
          responsive: false,
          scales: {
            x: {
              type: 'linear',
              position: 'bottom',
            },
          },
        },
      };
  
      const image = await canvasRenderService.renderToBuffer(configuration);
      res.set('Content-Type', 'image/png');
      res.send(image);
  
    } catch (error) {
      console.error('Error fetching data from MongoDB:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });

   // Start the Express server
  const PORT = 3000;
  app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
    });
  })();

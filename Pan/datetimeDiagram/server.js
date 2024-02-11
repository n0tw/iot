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
const readDataByTime = async(req, res, entityId, initYear, initMonth, initDay, initHour, initMinute, initSecond,
  endYear, endMonth, endDay, endHour, endMinute, endSecond, tz_offset) => {
  try {
    // Make an HTTP request to your Flask API endpoint
    const response = await axios.get(`http://localhost:5003/entities_by_time/${entityId}/${initYear}/${initMonth}/${initDay}/${initHour}/${initMinute}/${initSecond}/${endYear}/${endMonth}/${endDay}/${endHour}/${endMinute}/${endSecond}/${tz_offset}`);
    // Retrieve data from the Flask API response
    const responseData = response.data;

    console.log('Type of responseData:', typeof responseData);
    console.log('Content of responseData:', responseData);

    // Extract the 'data' array from responseData
    const data = responseData.data;

    console.log('Type of data:', typeof data);
    console.log('Content of data:', data);

    // Flatten the array of data to get individual entries
    const allEntries = data.flatMap(data => data);

    // Extract datetime and peopleCount values
    const xValues = allEntries.map(entry => entry.dateObserved.value['@value']);
    const yValues = allEntries.map(entry => entry.peopleCount.value);

    // Send the data as JSON
    res.json({ xValues, yValues });
  } catch (error) {
    console.error('Error fetching data from MongoDB:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

// Define a route to get data from MongoDB
const readDataAvgPeopleByTime = async(req, res, entityId, initYear, initMonth, initDay, initHour, initMinute, initSecond,
  endYear, endMonth, endDay, endHour, endMinute, endSecond, tz_offset) => {
  try {
    // Make an HTTP request to your Flask API endpoint
    const response2 = await axios.get(`http://localhost:5003/avg_people_by_time/${entityId}/${initYear}/${initMonth}/${initDay}/${initHour}/${initMinute}/${initSecond}/${endYear}/${endMonth}/${endDay}/${endHour}/${endMinute}/${endSecond}/${tz_offset}`);
    // Retrieve data from the Flask API response
    const responseData2 = response2.data;

    // Extract the 'data' array from responseData
    const data2 = responseData2.data;

    console.log('Type of data2:', typeof data2);
    console.log('Content of data2:', data2);

    const entries2 = Object.entries(data2);
    const xValues2 = entries2.map(([label, value]) => label);
    const yValues2 = entries2.map(([label, value]) => value);

    console.log('Type of xValues2:', typeof xValues2);
    console.log('Content of xValues2:', xValues2);
    console.log('Type of yValues2:', typeof yValues2);
    console.log('Content of yValues2:', yValues2);

    // Send the data as JSON
    res.json({ xValues2, yValues2 });
  } catch (error) {
    console.error('Error fetching data from MongoDB:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};

(async () => {
  // Enable CORS for all routes
  app.use(cors({
    origin: '*',
    credentials: true,
    allowedHeaders: ['Content-Type', 'Authorization'],
  }));

  // Read entity attribute
  app.get('/getDataByTime', async (req, res) => {
    try {
      // Add code to choose CrowdFlowObserved ID based on bus station

      const data = await readDataByTime(
        req,
        res,
        "urn:ngsild:CrowdFlowObserved:Station:2",
        2018,3,11,15,31,2,2024,4,5,1,5,2,0
        );
    } catch (error) {
      console.error('Error fetching data from MongoDB:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });

  app.get('/getDataAvgPeopleByTime', async (req, res) => {
    try {
      // Add code to choose CrowdFlowObserved ID based on bus station

      const data = await readDataAvgPeopleByTime(
        req,
        res,
        "urn:ngsild:CrowdFlowObserved:Bus:1",
        2018,3,11,15,31,2,2024,4,5,1,5,2,0
        );
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

// Function to fetch data from the server
async function fetchData(endpoint) {
  try {
    const response = await fetch(`http://localhost:3000/${endpoint}`, {
      mode: 'cors',
    });
    const data = await response.json();

    // Log the fetched data
    console.log(`Fetched Data for ${endpoint}:`, data);

    return data;
  } catch (error) {
    console.error(`Error fetching data for ${endpoint}:`, error);
  }
}

// Function to create and render the chart
async function createCharts() {
  try {
    // Fetch data for the first chart
    const data = await fetchData('getDataByTime');

    // Convert xValues to Moment.js objects
    const xValues = data.xValues.map(dateString => moment(dateString));
    //const xValues = data.xValues.map(dateTimeString => moment(dateTimeString));

    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: xValues,
        datasets: [{
          label: 'Average people in station per hour',
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
          },
        },
      },
    });

    // Fetch data for the second chart
    const data2 = await fetchData('getDataAvgPeopleByTime');

    const xValues2 = data2.xValues2;

    const ctx2 = document.getElementById('mySecondChart').getContext('2d');
    const mySecondChart = new Chart(ctx2, {
      type: 'bar',
      data: {
        labels: xValues2,
        datasets: [{
          label: 'Average people collected per station',
          data: data2.yValues2,
          borderColor: 'rgb(192, 75, 192, 0.2)',
          borderWidth: 2,
          fill: false,
        }],
      },
      options: {
        responsive: false,
        scales: {
          x: {
            type: 'category',
            position: 'bottom',
          },
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  } catch (error) {
    console.error('Error creating charts:', error);
  }
}

// Call the createCharts function when the page is loaded
document.addEventListener('DOMContentLoaded', createCharts);